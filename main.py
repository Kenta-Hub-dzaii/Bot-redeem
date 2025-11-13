#!/usr/bin/env python3
"""
Discord bot for bypassing shortlinks using MeoBypass API flow.
Slash command: /bypass url:<url>

Requirements:
 - discord.py
 - aiohttp
 - python-dotenv (optional)
 - aioredis (optional)

.env should contain:
BOT_TOKEN=...
BYPASS_API=https://api.meobypass.click
BYPASS_API_KEY=P0aTtED0HSuNX3WyNItH
REDIS_URL=
CACHE_TTL=86400
RATE_LIMIT_SECONDS=3
"""
import os
import re
import time
import asyncio
import logging
from typing import Optional, Dict, Any

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands

# load .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# optional aioredis
try:
    import aioredis
except Exception:
    aioredis = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("meobypass-bot")

# ----------------- Config from env -----------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
BYPASS_API = os.getenv("BYPASS_API")  # e.g. https://api.meobypass.click
BYPASS_API_KEY = os.getenv("BYPASS_API_KEY")  # your key
REDIS_URL = os.getenv("REDIS_URL", "")
CACHE_TTL = int(os.getenv("CACHE_TTL", "86400"))
RATE_LIMIT_SECONDS = int(os.getenv("RATE_LIMIT_SECONDS", "3"))

if not BOT_TOKEN or not BYPASS_API:
    logger.error("BOT_TOKEN and BYPASS_API must be set in environment (.env). Exiting.")
    raise SystemExit(1)

# ----------------- Constants -----------------
URL_REGEX = re.compile(r"https?://[^\s<>\"'`]+", re.IGNORECASE)
MEOBYPASS_POLL_INTERVAL = 2.0   # seconds between polling
MEOBYPASS_TIMEOUT = 60.0        # total seconds to wait for a result

# ----------------- Bot setup -----------------
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

# ----------------- Simple cache (Redis optional) -----------------
_memory_cache: Dict[str, Dict[str, Any]] = {}
_redis = None
_user_last_ts: Dict[int, float] = {}

async def get_redis():
    global _redis
    if _redis is None and REDIS_URL and aioredis:
        _redis = aioredis.from_url(REDIS_URL)
    return _redis

async def cache_get(key: str) -> Optional[Dict[str, Any]]:
    r = await get_redis()
    if r:
        val = await r.get(key)
        if val:
            try:
                import json
                return json.loads(val)
            except Exception:
                return None
    return _memory_cache.get(key)

async def cache_set(key: str, value: Dict[str, Any], ttl: int = CACHE_TTL):
    r = await get_redis()
    if r:
        import json
        await r.set(key, json.dumps(value), ex=ttl)
    else:
        _memory_cache[key] = value

# ----------------- MeoBypass call (kick + poll) -----------------
async def call_bypass_api(session: aiohttp.ClientSession, url: str, timeout: int = 20) -> dict:
    """
    MeoBypass flow:
      1) GET {BYPASS_API}/bypass?url={url}&api_key={BYPASS_API_KEY}
         -> { "status": "pending", "task_id": "..." }  (or success immediately)
      2) GET {BYPASS_API}/taskid/{task_id}
         -> { "status": "success", "result": "https://final..." }
    Returns dict: { "finalUrl": "...", "meta": {...} }
    Raises RuntimeError on failure/unsupported/timeout.
    """
    if not BYPASS_API:
        raise RuntimeError("BYPASS_API not set")

    base = BYPASS_API.rstrip('/')

    params = {"url": url}
    if BYPASS_API_KEY:
        params["api_key"] = BYPASS_API_KEY

    # 1) start task
    try:
        async with session.get(f"{base}/bypass", params=params, timeout=timeout) as resp:
            text = await resp.text()
            if resp.status >= 400:
                raise RuntimeError(f"API error {resp.status}: {text}")
            try:
                j = await resp.json()
            except Exception:
                raise RuntimeError(f"Unexpected non-JSON response from bypass endpoint: {text[:200]}")
    except Exception as e:
        raise RuntimeError(f"Failed to call bypass endpoint: {e}")

    # parse response
    status = (j.get("status") or j.get("state") or "").lower() if isinstance(j, dict) else ""
    # immediate final?
    if status == "success":
        final = j.get("result") or j.get("finalUrl") or j.get("final") or j.get("result_url")
        if final:
            return {"finalUrl": final, "meta": j}
        raise RuntimeError("API returned success but no result field")

    # if no status field, maybe returned final directly
    if not status:
        final = j.get("result") if isinstance(j, dict) else None
        final = final or (j.get("finalUrl") if isinstance(j, dict) else None)
        if final:
            return {"finalUrl": final, "meta": j}
        raise RuntimeError(f"Unexpected response shape: {j}")

    if status != "pending":
        # unsupported or failed
        reason = j.get("error") or j.get("reason") or str(j)
        raise RuntimeError(f"API returned status={status}: {reason}")

    task_id = j.get("task_id") or j.get("taskid") or j.get("id")
    if not task_id:
        raise RuntimeError(f"Pending response but no task_id: {j}")

    # poll loop
    deadline = time.time() + MEOBYPASS_TIMEOUT
    while time.time() < deadline:
        try:
            async with session.get(f"{base}/taskid/{task_id}", timeout=timeout) as r2:
                txt2 = await r2.text()
                if r2.status >= 400:
                    raise RuntimeError(f"Task-check API error {r2.status}: {txt2}")
                try:
                    j2 = await r2.json()
                except Exception:
                    raise RuntimeError(f"Non-JSON from task endpoint: {txt2[:200]}")
        except Exception as e:
            # transient error: wait then retry
            await asyncio.sleep(MEOBYPASS_POLL_INTERVAL)
            continue

        st2 = (j2.get("status") or j2.get("state") or "").lower() if isinstance(j2, dict) else ""
        if st2 == "success":
            final = j2.get("result") or j2.get("final") or j2.get("finalUrl") or j2.get("result_url")
            if final:
                return {"finalUrl": final, "meta": j2}
            raise RuntimeError(f"Task succeeded but no result: {j2}")
        elif st2 in ("pending", "processing", "queued"):
            await asyncio.sleep(MEOBYPASS_POLL_INTERVAL)
            continue
        else:
            reason = j2.get("error") or j2.get("reason") or str(j2)
            raise RuntimeError(f"Task failed/unsupported: {reason}")

    # timeout
    raise RuntimeError(f"Timeout waiting for MeoBypass task result ({MEOBYPASS_TIMEOUT}s)")

# ----------------- Helpers to build embed & button -----------------
def build_embed(original: str, data: Dict[str, Any]) -> discord.Embed:
    final = data.get("finalUrl") or data.get("meta", {}).get("result") or "Unknown"
    hops = data.get("meta", {}).get("hops") or []
    embed = discord.Embed(title="Bypass Result", color=0x1abc9c)
    embed.add_field(name="Original", value=f"[Original Link]({original})", inline=False)
    if isinstance(final, str) and final.startswith("http"):
        embed.add_field(name="Final", value=f"[Open final link]({final})", inline=False)
    else:
        embed.add_field(name="Final", value=str(final), inline=False)
    if hops:
        hop_text = " → ".join(hops[:10])
        if len(hops) > 10:
            hop_text += " …"
        embed.add_field(name="Hops", value=hop_text, inline=False)
    note = data.get("meta", {}).get("note")
    if note:
        embed.set_footer(text=str(note))
    return embed

class OpenUrlView(discord.ui.View):
    def __init__(self, final_url: str, timeout: Optional[float] = 180.0):
        super().__init__(timeout=timeout)
        if isinstance(final_url, str) and final_url.startswith("http"):
            self.add_item(discord.ui.Button(label="Open final link", url=final_url))

# ----------------- Slash command -----------------
@app_commands.describe(url="Link rút gọn hoặc link cần giải")
@tree.command(name="bypass", description="Gọi MeoBypass API để bypass link rút gọn. Usage: /bypass url:<url>")
async def slash_bypass(interaction: discord.Interaction, url: str):
    await interaction.response.defer(thinking=True)

    # validate url
    m = URL_REGEX.search(url.strip())
    if not m:
        await interaction.followup.send("❌ Không tìm thấy URL hợp lệ. Vui lòng nhập URL bắt đầu bằng http/https.", ephemeral=True)
        return
    url = m.group(0)

    # rate limit per user
    uid = interaction.user.id
    now = asyncio.get_event_loop().time()
    last = _user_last_ts.get(uid, 0)
    if now - last < RATE_LIMIT_SECONDS:
        await interaction.followup.send(f"Bạn gửi quá nhanh — chờ {RATE_LIMIT_SECONDS}s giữa các yêu cầu.", ephemeral=True)
        return
    _user_last_ts[uid] = now

    # cache check
    key = f"unshort:{url}"
    cached = await cache_get(key)
    if cached:
        data = cached
    else:
        try:
            async with aiohttp.ClientSession() as session:
                data = await call_bypass_api(session, url)
            await cache_set(key, data)
        except Exception as e:
            # return error message (ephemeral)
            await interaction.followup.send(f"❌ Không thể bypass link này: {e}", ephemeral=True)
            return

    # success -> build embed + button
    final = data.get("finalUrl") or (data.get("meta") or {}).get("result")
    if not final:
        await interaction.followup.send("❌ API trả về dữ liệu không có final link.", ephemeral=True)
        return

    embed = build_embed(url, data)
    view = OpenUrlView(final_url=final)
    # public response; change ephemeral=True if you want private
    await interaction.followup.send(embed=embed, view=view)

# ----------------- on_ready: sync commands -----------------
@bot.event
async def on_ready():
    try:
        # For instant testing in a single guild, change to:
        # await tree.sync(guild=discord.Object(id=YOUR_TEST_GUILD_ID))
        await tree.sync()
        logger.info("Slash commands synced.")
    except Exception as e:
        logger.warning(f"Failed to sync global commands: {e}")
    logger.info(f"Logged in as {bot.user} (id: {bot.user.id})")

# ----------------- Optional: keep message handling for other features -----------------
@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    await bot.process_commands(message)

# ----------------- Run -----------------
if __name__ == "__main__":
    bot.run(BOT_TOKEN)

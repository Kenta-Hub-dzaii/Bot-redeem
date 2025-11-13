from flask import Flask, request, jsonify
from discord.ext import commands
import discord
from datetime import datetime, timedelta
import json
import os
import random
import string
import threading
import asyncio

# ==================== CẤU HÌNH ====================
BOT_TOKEN = 'MTQzMDg4NTkyNTg4NTU3NTM0MA.GkVyfp.JpZ0DV9M51LI1UF-tcVfDSvBRyqtxVf8uq0S6s'
API_BASE_URL = 'http://localhost:5000'
WHITELIST_ROLE_ID = 1436965081123524750  # Thay bằng role ID thực tế

# ==================== KHỞI TẠO FLASK ====================
app = Flask(__name__)

# ==================== KHỞI TẠO DISCORD BOT ====================
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# ==================== QUẢN LÝ DỮ LIỆU ====================
DATA_FILE = 'data.json'
KEYS_FILE = 'keys.json'

def init_data():
    """Khởi tạo dữ liệu nếu chưa có"""
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump({"whitelisted": {}}, f)
    
    if not os.path.exists(KEYS_FILE):
        initial_keys = "6EprP0,ysocsJ,O4mhyo,y4m3f9,tf3C9u,pi2opy,eR1Rah,ZGKKOP,o4lhJT,OWrS2C,ObfWmQ,AxRpfv,QEEwUx,YyKAoX,QKqnNX,WVtMrS,dtU3OH,ajNyFS,jNeBsz,Pp6lsM,pLZYwt,MhPbdp,yd0dxV,gnasTz,pfbm1Y,7UKDkh,4E78RT,xJP3Md,6MQcAP,xlMC5J,NiIzSD,zcIXbU,uXazsP,alORTc,RWDN0u,d1JDCd,tVMLes,9xgyVn,YQ4n1N,mSkqtG,hDoGTM,VrLJpa,WqM8dQ,ijEjVS,Gioee7,DWQBjD,s22rX5,l3HCsk,yZ2TuR,5QvkZt,I7FctB,VPgREV,QAe5YB,6vUeIo,svS85x,deZicE,EZXsFb,laxYQd,e5oBQi,uIevZC,mZjjEL,LNOmGy,NneKie,GwqFHy,AvxU0Z,2q1wG4,f8UNTF,bT9bLx,No4kvB,hTsKDI,lMjY7s,kB0zeK,96F6Kr,xdeSRt,uY85cG,yTwELJ,XYGGez,DwyGTj,SdTU8R,ywkfa5,9yLwEN,i6Ym34,qBWDJj,ln996w,aMdTKt,wrkOoZ,uPlNdo,ZIxXHf,bKl4qF,c8oVgh,EP6obp,BkWvKM,983drs,M56G4t,8g7O97,VQnm6D,lfm41m,6vNMqH,JKhDuC,1ZTx7F,ULtJ5J,Hl6YEJ,IQXuJT,moAYka,Bl7sA2,npxHpr,6E3pfA,ExGMnL,b4tuTO,m80hDB,qeaRI9,H2r2sy,e4bFF1,LhZKeu,A14WsV,NDCn4m,BjqTOp,N8eF3l,sz9vSE,JuTu7v,JaMEp0,S9qqWh,kafNV6,eIap3J,oqyFLR,gi6h47,CAag3j,xiWs4A,GKDPKm,SwWIq3,wFBQk3,ES4SO3,eRvDT8,iZRlio,5tdzi6,J1alhP,sb5uWH,zW4HRl,2RD3cT,48n2ep,IkQgUS,o8cYk3,gB3dTc,EWeo5Q,mnCyJN,z5yyTd,Er5LGs,aZCqtN,6cOKpa,6gqbtd,GYlCW5,qi7aoE,JcivuH,mxIsLl,2ulycJ,hEQnBn,gaNid0,3UOzPo,aYcbyG,ajDJgg,gcoYJy,u484Nm,CUqMRJ,SH2mKd,NJaltG,BuoI4q,6f3NJT,Xojt7X,DFZRON,JzmhwJ,O1diIA,kIx66f,3rDHU8,yCb9dD,6bFMSO,slYMfS,vgL2co,RZGkhg,aYCrqj,BHxNhk,SbfA8s,Vf9lEO,OMCH89,7D31jL,pqaaUM,TJvxVE,3tdnN9,ADmJLf,ugwft7,diXnXS,gsE4dX,95xp4J,AKPTfC,Oem1Ue,2JZLJj,iXZJAm,ZATMg2,KXFwe8,jMSIXL,C8PZWh,YOn3qX,2G3puN,7LfJ2p,uJcmYn,uUyCWd,C5tVrT,y0T5Ex,Icuibe,FFusXa,76DzSf,GU9TQE,955GE3,dA6NCB,M2meJY,eBCQjX,P4oa4n,xQ1NAW,fViXZf,zrqr6O,pi11Ra,qYqJFU,2zS2LC,Up5oqa,gJuwWD,MTHMxT,xWt2GJ,Lslcmx,st5Mon,aXosan,Mbr9QM,BkU0T3,Xh29CH,oScCAA,cfSfut,N9Ela5,fJSQv0,09DoIo,rK8IAG,4GD7fw,fpgDcE,VZ3gnq,C0ERU9,oatwtO,cDHpNf,TIXWRR,CK52fw,0rs50J,7RMG7O,uZGCRt,OB5SZc,pLFL44,cVrSiS,e1jApJ,xgE3NL,fBqumi,ly0GvZ,S3TGeV,FCQNGa,zBVFDB,UpWfgY,9QG44L,EBFcGr,uc0rgX,zy3I51,BVPmy5,bxscDY,FYtmPC,D3e6oQ,gxz05f,bRm52w,odvqpL,0sMCHv,m2VDa3,nqvwQK,30UDoP,6mzIyO,3zYX6o,ebwfjR,cf75es,FyWVoH,Wz8dCW,g6WGMN,OIG2H9,aHDp4c,gm2DoH,93NYbh,VCxMcs,x3UvLE,wxG4DQ,EVZTvO,6DVlJV,1uzi9y,DZRRMX,1LWQm4,7SiIY7,c624WG,pkBYDS,Gb3uB7,LiXyI0,BXE88Y,4QBDDK,8Bx9Pu,pOEVUS,bkweiU,X88arb,G2BGwm,42nAUL,ogcKFS,KWa47X,9bahkp,vKekgt,nzpBSo,d9HTNk,jyU7o8,laWGA9,6Ln0i7,2drTYr,tHBTxJ,OaR3xD,UxtQyP,mU50bR,YZcuVc,rYQV0O,fSCyJt,ZEzn14,TD1Lcx,Pk1l6U,h9xqDy,VJFpMY,6qfaIY,ApDSmr,ii8Kol,potzPJ,Nu78go,Zf23OM,056PRv,eLBnWq,qdeo7S,efrDj1,c3oczf,mMtaQc,R473Iw,Hy1u4B,IFMD4d,835c7z,W8mrgW,x3NhBP,dfoXAt,SNkKzy,S30xO6,Fq7XyF,oj5w2z,ZmDFzv,hHXHAJ,orxnSj,9hw0AZ,it6l1t,zuHkoi,98VEid,s5EJxN,fH0abp,pqyFDM,8GPG3M,YuY1d9,jYQZHk,BW5TP3,nTQxZx,bS7XZ8,N1yFuS,tfBg07,dp5aVV,4bfsh6,uJphWI,cTNF7E,GbQ9Ql,nDb6GW,Dv2kM8,9d0HYr,AZCL85,ZEJpQb,c8lSzj,ZBGuJs,z3dMFR,7623Yf,3ViSWJ,ovxWZU,pCLUjs,eDG3k8,8nktn3,4blujv,K8TVei,Li9IoT,2VmxG6,ISUvTl,Oz8elS,F3d5no,LXVZA4,rBTcaw,QeWeVA,QW9ov1,nuhLpr,Hh5OEV,J5myY9,SkdT93,lYkTh4,60vNBs,KDaW2t,82C3jX,bDV8A9,ZrS52g,yFeKTW,APgrXU,RkN0O4,PW0NUg,ybb3a5,Sud5uP,OvKAW7,ZTYv0w,nG43BF,97k1yj,74jkPp,xUllCA,hdM1Re,zE4Msp,VlW5DG,nn8TPa,mjXow2,doUNbN,XupHod,IJDZj5,EQYUsE,zoOTDX,zVho98,bL0ULP,FcbL5b,4fpIDQ,33MnTk,S90I2G,Ra51FX,L5MO8p,8vRm5P,Dy053y,wLgbKU,UOylVE,mn6g45,HGtjk5,JSGvrG,2mpqgl,5EsTh4,enw62Y,RwXkAl,ec93Es,nAEb8w,7Snzqm,1yBBtp,uqejKe,9J0dtR,WW2OLd,jOoNVB,yp1Eaf,4AipwG,HGqKyy,TYxAFq,fgvLka,exeYCf,OwqDRU,rfGG7Z,UWgp8P,HgNgqD,6m5pfk,WOLC3y,jVVWUh,jd9SXZ,lbL8Gn,xuBQIK,9OoQUP,YnkmjX,n8nlIJ,4CV7wY,yn1snF,kf3EP0,dzqEG3,CSVznf,dj26DQ,67C4eV,yZlFGo,HkZbGN,NKIKg7,kp74Xa,AjkE3C,JL9NG6,28L6ga,bceWAs,kzMBE1,PdYjND,P31ipn,um1aqA,bo97Uq,vfbTNr,TjqoLp,r9Rp1s,wVQKOY,9cTsG6,ro8ul5,ve1OgS,KMM0yT,JKnju1,v5ZLnh,2ogZtW,sgcq1T,37nBMK,oOtpnt,3I6IRq,HPeuwi,yTt2f2,kHPToz,6MiFtS,9DmAkZ,hQFs2K,owIQti,kqySE8,N4idXl,yWWR84,yCVfaE,q6XpnV,0v2JlS,1vUgTI,1j01Jr,sRhcoB,bPpUAW,6GYEeF,gMWM27,YGDlyJ,4DVk17,eWqZ66,6YGMPw,C9C04b,I00GFu,J9LSSd,Y2oanf,izYvHE,QeErBr,DWeXFk,ge6wTC,Nf5MzO,JYGDj8,gulhwx,oWvhgQ,LazHlk,lZJDIg,PGXy2Q,cc9KJz,nDV2Fq,dMWju8,LASHRf,cba9MU,NtT3eZ,EZ9VpW,MWKP82,ODMPLg,c4s4MH,i25tHw,llE58c,V6Zf05,Y8uTzB,bI9ifP,zfqk0F,03uuDU,gby76J,NUGofl,Cf8cMM,tGYpc1,9JISTO,ICsFaD,5GXzuR,QwR9Wi,pKvJgS,Bhnmx0,2F7XFD,ewlt2c,x8X8XU,dUzAqG,R48r51,1SJ6pw,WdbC42,qM97PR,YdMPwO,0WTAQY,7U4qHH,qTuWUS,8PiiJb,1xdxyX,bZZDuS,L8mBwK,41y2t1,44yGWV,2MyxVX,gRC6Zs,0m1Wtc,f4GXac,pv5P9e,chjVdR,dwgt1k,f3KtUr,lmwZoO,uzrosG,0qi17e,ZNu5fH,tgDdUK,N6JaCw,LCTawY,LRvUMX,0WtqkS,LvZ9PQ,Rge35N,lCmZH1,uAQPcn,Y16aXB,HAYa0G,yQMJJY,VcClUP,Xtk8dT,SYWDbI,3THhsL,RbswTK,6aZjio,o7sFob,mt1Edt,VLofbg,09O3Xp,RtiPFV,BDC1hp,hYULql,mSZ3PG,xFEz1X,YYFsdq,WaMnXL,aQ4aT3,QJP7jz,YNUP1F,5JTsSf,c0ZG9W,6lLK7C,SyjY81,wfxgyp,g3YZDI,Rupf47,cZOmQw,6pUq6h,pvcnOC,GwOcgf,GfroDi,NIpnUe,ZSCk5S,72giKX,DR7f8X,6jGmzj,BxgtK5,8wQhWu,KFT9sG,jkHejx,TtR9en,QEhW2T,ZElm4E,wVHOeo,4qltBJ,yUkBB9,mzwYlY,gVMxmX,8dQrJr,LLbSnp,KdL1Hx,tW2Qpj,p6kMdk,l1rgGF,QvZVcC,7lKCas,iZ65bG,0ANsAy,zdHWzk,rrc0O0,F3VPea,G7aiOl,Cq7LPu,gmqRer,0S2Xts,ChU6a9,e2CLZO,07ao3o,qiR7x8,9JPUUf,ffUQG2,STxGI8,MdZKrB,mfL1rw,sfxRZ4,N6DQ0J,eMfEOo,nipp7w,701Z1U,VAelyK,rdbKUF,FEn6gI,GlT2mt,MxhV0A,KpwVXh,GaUjYn,xlArlj,I1aZ2J,5mT8o2,aj9Jcv,GYGZ0B,sKyear,x3749t,UspY3P,fiCJtC,Q1RWSz,IlqbaQ,Gx6oTH,tg6KuG,qwSJPh,v5F88Z,4o0Y3E,ZMpUlN,IrFImb,M52sZQ,ptgoXQ,4NoAbA,3hXR6b,e94RRv,KfYoDB,1gl43i,MadxRF,pB5QrI,EphecI,osCHx0,fHm9h1,3sY4Ku,LjM10f,p7gXO9,9YfVQR,lqx6AK,N8WQ44,hqjOJ9,OiKvC1,OXoKlR,dfApPr,18zXG7,SsARrw,6gdf9o,tqBBkk,Su5jcV,qr2jh5,uv69VI,TEuaaU,qAfC1A,wTmRcW,G1YSoS,CrJ6H1,DhGM5Z,dV1aRy,iMovyL,a2Lb9T,Pu0oFZ,VSn30L,wi2akH,Pkz66o,DYaBMw,VXkZbj,VJeHrl,aiD3Hp,fC4h6s,lo8G7b,EOSqfr,PNi8Hc,ZGdAgI,bdTRFc,w9z1sS,gZblqg,RLk0NX,yvQkau,Q0VBZT,s5II7j,PLLNDF,Dm5Ct4,VvP9yl,KlbV80,KPpOqU,kchfIM,VWMXs0,FbwLS4,bfuHVN,dApgfO,C19nG6,DUVedn,iU97HO,qeJLq8,ZTtnvi,UMykTa,on1lal,uSUFze,GmgPmD,rjzyCV,zdCao7,JB3Jl8,Jkofox,JQ8Vd1,LdOGBU,0FZPu4,WuRfxD,l9Khlp,MTjLrx,nlk4s0,Y4dNnj,Es4M8x,OX9S5i,XUcyXQ,Hnj3lk,vxyuzK,W0AT6J,weLJTN,KMp4YB,qO61bz,0VpAZS,2GyhZT,8clydc,Y6wvnx,EI2nNS,2utl8a,MwvxSK,LeZhK7,aSGwII,mv94n8,EHEuqg,suP4yY,fEhOj2,hS29ZO,7Vdg0z,Ed6HGw,hVyDlm,GGlMMu,5dr4lI,M88eTz,frnFT5,5ctEsA,K56Wbf,9TlSh9,QgxiAX,nI5JsR,2VRAyW,i6hLju,WLH5Hv,atImKs,S2He51,psjkBV,vSLgui,NzsIeO,2pAIKm,aWASjV,wagV7M,fqWKXT,dHclC7,iOlt7M,A26oN1,24uGkS,it45ws,u5CHlG,6y4lLK,lxO3CP,3R0WNK,csM9r4,FJsFbV,X2dQk5,KbzYGz,aB1qQr,gvG7Wl,b2Vmnq,YNAL0v,yrVrSf,VOGYSu,CH68xF,QBuBup,wHTGnC,g4GGya,cHhp3V,3SsZIW,qzNYUw,HYbEeq,EFPRzD,HQfLuN,mvZedf,rA6H2w,vrc4LH,diFvAe,U3QMo8,N5bYcn,2HMnSa,0Ls1ik,r7Ewyd,JOIdRz,7JMX5g,9vlkmk,DDjuoA,BBPyLI,WGS2Du,3rHF1s,M9Y6k7,zfebLa,rZ0UHJ,YmVVgr,foDrYu,U6iuwN,d7nSb2,RE1OMa,eXBqAs,EKACqK,GtKeXf,Cs520b,PE7yoG,KNAAby,zMhKRI,kKlTrx,TQWU2Y,emJ62H,zDhulL,rboXWF,xAk5X2,xDJOUe,lgzhnO,wTA75m,zr12Xo,oTkxVE,BeAnLu,qUeHhg,FQqtvK,R3aMSi,R6EHpE,trSgQ4,QbOmr9,9MuH2e,d96Hsj,GtBs5N,jOA7aQ,prJ547,IGg30W,VbJbdv,AQQy97,Xmk5Mt,4ZeTED,S4Duad,w4Aptv,djoNWA,u4A7ZV,fqu4L1,RdYDtA,8WE7u1,EZM1zs,5KiBmu,rod0rE,HLSG1J,ZbGq3W,2lqSRs,mU1Onr,v9doHe,ktfG7p,Lw8tXD,EvjRvz,mRSFwF,Q0u15B,M1kc3j,2sF67P,vimHpY,9DTMl2,ExfT9o,3zTv04,RUUASj,iNfkKU,sdd0LA,ui3vAA,LHw0FM,4jGPh7,7RiPCY,s2o26R,ogc6zx,MaAifH,0sh7Sw,bavdaW,97ebVq,zeB0GZ,bj0O5N,zauW1u,6Unved,2MjUoB,gv98Wy,oK7tFg,j3IXxW,HluQJ4,RPQxNs,LLgNnJ,e7HxUX,Qq2UtT,pyTqx1,n95DNg,WVBTdg,6ECK6v,PDWRs0,uRA4Ac,RP9FSb,N42avm,MKzDHY,CXl9JH,ovQtKS,Ki3EiG,iKVbdM,B4xjMU,sSnOYf,dDwEzs,3nGY7S,ubXXLH,nn81D1,i5tHrg,gm5W5R,0jx4Z3,iVEIU1,gFAZnV,Q5julw,wWF1t7,E6hMxU,63re4U,iiXblX,2WfixY,mDNZy9,4aG20X,OcUcV7,pvJiUe,Gwxydl,bpYyfy,cPYdN4,KMyfwm,bzmnqd,iCdtud,XUPs4s,62Cog5,Epl2F1,FMWhIo,faI9Ay,t3JWpr,aievjT,rPLTuM,XGi3kX,ZvrJMu,E6VJTF,HcUdE6,uDQpIt,s8iwgH,xyLW74,B4Y8yj,3YFEEG,JFftWv,2TAAjT,Xq6ezq,Yjp2Fg,WGbPuy,GM1rdI,Ds32Fm,fqKb7e,wkncTv,N9fRjL,xZRhGe,sSM2qD,myj0Ml,r0IZWL,IbOgKb,E47XOs,4O9RSJ,8Pmyel,6qlJBQ,3eEvvO,8geqc4,qaj0cS,VdWavN,AsEy94,w1SYcA,rQvUnW,b2RHVs,bHQ3Ad,yUx4KA,6THq3i,lWwZlO,qRxiYj,SjF8fW,7W1rnB,GcA7Zm,bWdA2a,Vtabig,C5K1ZC,itYkar,GPx3Qq,ZjuRrU,p32fQf,v13GHM,MuTkHt,PfeIEY,pzfvlU,UisCJo,B2K3Vh,F67lC2,l4KtXg,Z4Tw3a,1Aw64d,6SAWLZ,9zFCBN,ff8RPr,CDLwsS,QDVs4l,ynp8L6,2t08z7,31AWSu,w42irO,gR25JZ,RjBK0A,jUz8Bx,w8d3wL,sNioYZ,MVJr9v,KQ523F,nwYZVB,jAyFWA,q2MXEP,Ikmcfj,aK0eff,MsuzLK,OcEMi1,8LOhbO,FNjDwU,ZU0A0I,9W1KKf,30RXQ7,Phk9wr,6eHtXi,2PZKr2,dMUSm9,1XlKmq,TFH19h,UbIuzF,k2ktTP,miWczR,JMD98k,zllvPf,WLQV8b,Aort9f,KvFs89,fJeLeA,7VOcEy,xg8UVq,i4mPyW,ZT3qu0,XVKswA,mlWq4p,Z8T89a,3fBzL0,mg7tgW,cOc9ou,dyVjTl,eQeuMI,QEXCwz,C9mPNB,LlnDpD,ZHrQXj,2meyO7,F3B7Re,meX40c,CQfEsR,MGYNHT,prJ3A8,2v14Ta,0YRcys,jo5O2P,gJkvY1,26huUU,FgmcHb,mVLG4P,qa8yg4,kFI3pb,IVl4jO,rxlmBR,5UrFgZ,O4Ed7M,uUtDZa,3M0pjg,h41yw5,LWaFev,b0nYRH,i4tNTX,31L7Vl,i8fZjv,KrTDfO,4Bju3V,AX2bYC,EJ0UGR".split(',')
        with open(KEYS_FILE, 'w') as f:
            json.dump({"available_keys": initial_keys, "used_keys": {}}, f)

init_data()

def generate_random_key():
    """Tạo key ngẫu nhiên dạng Kenta-xxxxx-xxxxx-xxxxx-xxxxx"""
    parts = []
    for _ in range(5):
        part = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
        parts.append(part)
    return '-'.join(parts)

def get_current_time():
    """Lấy thời gian hiện tại UTC+7"""
    return datetime.utcnow() + timedelta(hours=7)

def make_api_request(endpoint, method='GET', data=None):
    """Hàm helper để gọi API nội bộ"""
    url = f"http://localhost:5000{endpoint}"
    try:
        if method == 'GET':
            response = requests.get(url)
        elif method == 'POST':
            response = requests.post(url, json=data)
        elif method == 'PUT':
            response = requests.put(url, json=data)
        elif method == 'DELETE':
            response = requests.delete(url)
        
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# ==================== FLASK ROUTES ====================
@app.route('/')
def home():
    return jsonify({"message": "Flask API + Discord Bot is running!"})

@app.route('/whitelisted', methods=['GET'])
def get_whitelisted():
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/whitelisted/<user_id>', methods=['GET'])
def get_user(user_id):
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    
    if user_id in data['whitelisted']:
        return jsonify(data['whitelisted'][user_id])
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/whitelisted', methods=['POST'])
def add_user():
    user_data = request.json
    user_id = user_data.get('userid')
    
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    
    if user_id not in data['whitelisted']:
        random_key = generate_random_key()
        data['whitelisted'][user_id] = {
            'userid': user_id,
            'lasthwidreset': None,
            'hwid': None,
            'key': random_key,
            'blacklist': False
        }
        
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        
        return jsonify({"message": "User added to whitelist", "key": random_key})
    else:
        return jsonify({"error": "User already exists"}), 400

@app.route('/whitelisted/<user_id>', methods=['PUT'])
def update_user(user_id):
    user_data = request.json
    
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    
    if user_id in data['whitelisted']:
        data['whitelisted'][user_id].update(user_data)
        
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        
        return jsonify({"message": "User updated successfully"})
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/whitelisted/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    
    if user_id in data['whitelisted']:
        del data['whitelisted'][user_id]
        
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        
        return jsonify({"message": "User removed from whitelist"})
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/keys', methods=['GET'])
def get_keys():
    with open(KEYS_FILE, 'r') as f:
        keys_data = json.load(f)
    return jsonify(keys_data)

@app.route('/redeem', methods=['POST'])
def redeem_key():
    data = request.json
    key_to_redeem = data.get('key')
    user_id = data.get('userid')
    
    with open(KEYS_FILE, 'r') as f:
        keys_data = json.load(f)
    
    if key_to_redeem in keys_data['available_keys']:
        # Xóa key khỏi available_keys
        keys_data['available_keys'].remove(key_to_redeem)
        
        # Thêm key vào used_keys với userid
        keys_data['used_keys'][key_to_redeem] = user_id
        
        # Tạo key mới và thêm vào available_keys
        new_key = generate_random_key()
        keys_data['available_keys'].append(new_key)
        
        with open(KEYS_FILE, 'w') as f:
            json.dump(keys_data, f, indent=4)
        
        # Cập nhật whitelist
        with open(DATA_FILE, 'r') as f:
            whitelist_data = json.load(f)
        
        if user_id not in whitelist_data['whitelisted']:
            whitelist_data['whitelisted'][user_id] = {
                'userid': user_id,
                'lasthwidreset': None,
                'hwid': None,
                'key': new_key,
                'blacklist': False
            }
        else:
            whitelist_data['whitelisted'][user_id]['key'] = new_key
        
        with open(DATA_FILE, 'w') as f:
            json.dump(whitelist_data, f, indent=4)
        
        return jsonify({
            "message": "Key redeemed successfully", 
            "new_key": new_key,
            "user_id": user_id
        })
    else:
        return jsonify({"error": "Invalid key"}), 400

@app.route('/verify', methods=['POST'])
def verify_key():
    data = request.json
    key_to_verify = data.get('key')
    hwid = data.get('hwid')
    
    with open(DATA_FILE, 'r') as f:
        whitelist_data = json.load(f)
    
    # Tìm user có key này
    for user_id, user_data in whitelist_data['whitelisted'].items():
        if user_data.get('key') == key_to_verify:
            if user_data.get('blacklist', False):
                return jsonify({"valid": False, "reason": "User is blacklisted"})
            
            if user_data.get('hwid') is None:
                # Lần đầu sử dụng, lưu HWID
                user_data['hwid'] = hwid
                with open(DATA_FILE, 'w') as f:
                    json.dump(whitelist_data, f, indent=4)
                return jsonify({"valid": True})
            
            if user_data.get('hwid') == hwid:
                return jsonify({"valid": True})
            else:
                # Check if HWID reset is allowed
                last_reset = user_data.get('lasthwidreset')
                if last_reset:
                    last_reset_time = datetime.fromisoformat(last_reset)
                    if get_current_time() - last_reset_time < timedelta(day=1):
                        return jsonify({"valid": False, "reason": "HWID reset cooldown"})
                
                return jsonify({"valid": False, "reason": "HWID mismatch"})
    
    return jsonify({"valid": False, "reason": "Key not found"})
    
# ==================== DISCORD SLASH COMMANDS ====================
@bot.event
async def on_ready():
    print(f'✅ {bot.user} has connected to Discord!')
    print(f'✅ Flask API is running on http://localhost:5000')
    
    # Đồng bộ slash commands
    try:
        synced = await bot.tree.sync()
        print(f"✅ Đã đồng bộ {len(synced)} slash commands")
    except Exception as e:
        print(f"❌ Lỗi đồng bộ slash commands: {e}")

@bot.tree.command(name="redeem", description="Redeem key để nhận quyền truy cập")
async def redeem_key_cmd(interaction: discord.Interaction, key: str):
    """Lệnh redeem key"""
    user_id = str(interaction.user.id)
    
    # Gọi API để redeem key
    result = make_api_request('/redeem', 'POST', {'key': key, 'userid': user_id})
    
    if 'error' in result:
        await interaction.response.send_message(f"❌ Lỗi: {result['error']}", ephemeral=True)
    else:
        # Thêm role cho user
        try:
            role = interaction.guild.get_role(WHITELIST_ROLE_ID)
            if role:
                await interaction.user.add_roles(role)
        except Exception as e:
            print(f"Error adding role: {e}")
        
        await interaction.response.send_message(
            f"✅ Redeem thành công! Key của bạn: `{result['new_key']}`", 
            ephemeral=True
        )

@bot.tree.command(name="script", description="Lấy script để sử dụng trong game")
async def get_script(interaction: discord.Interaction):
    """Lệnh lấy script"""
    user_id = str(interaction.user.id)
    
    # Kiểm tra whitelist
    user_data = make_api_request(f'/whitelisted/{user_id}')
    
    if 'error' in user_data or user_data.get('blacklist', False):
        await interaction.response.send_message(
            "❌ Bạn không có quyền sử dụng script!", 
            ephemeral=True
        )
        return
    
    key = user_data.get('key', '')
    
    script_code = f'''getgenv().Key = "{key}"

loadstring(game:HttpGet("https://raw.githubusercontent.com/your-repo/script/main/verify.lua"))()'''
    
    await interaction.response.send_message(
        f"```lua\n{script_code}\n```", 
        ephemeral=True
    )

@bot.tree.command(name="resethwid", description="Reset HWID của bạn")
async def reset_hwid(interaction: discord.Interaction):
    """Lệnh reset HWID"""
    user_id = str(interaction.user.id)
    
    # Lấy thời gian hiện tại UTC+7
    current_time = datetime.now().isoformat()
    
    # Cập nhật last HWID reset
    result = make_api_request(f'/whitelisted/{user_id}', 'PUT', {
        'lasthwidreset': current_time,
        'hwid': None
    })
    
    if 'error' in result:
        await interaction.response.send_message(
            f"❌ Lỗi: {result['error']}", 
            ephemeral=True
        )
    else:
        await interaction.response.send_message(
            "✅ HWID đã được reset! Bạn có 1 phút để set up lại.", 
            ephemeral=True
        )

@bot.tree.command(name="whitelist_add", description="Thêm user vào whitelist (chỉ admin)")
@commands.has_permissions(administrator=True)
async def whitelist_add(interaction: discord.Interaction, member: discord.Member):
    """Thêm user vào whitelist"""
    user_id = str(member.id)
    
    # Thêm vào API
    result = make_api_request('/whitelisted', 'POST', {'userid': user_id})
    
    if 'error' in result:
        await interaction.response.send_message(
            f"❌ Lỗi: {result['error']}", 
            ephemeral=True
        )
    else:
        # Thêm role
        try:
            role = interaction.guild.get_role(WHITELIST_ROLE_ID)
            if role:
                await member.add_roles(role)
        except Exception as e:
            print(f"Error adding role: {e}")
        
        await interaction.response.send_message(
            f"✅ Đã thêm {member.mention} vào whitelist với key: `{result['key']}`"
        )

@bot.tree.command(name="whitelist_remove", description="Xóa user khỏi whitelist (chỉ admin)")
@commands.has_permissions(administrator=True)
async def whitelist_remove(interaction: discord.Interaction, member: discord.Member):
    """Xóa user khỏi whitelist"""
    user_id = str(member.id)
    
    # Xóa khỏi API
    result = make_api_request(f'/whitelisted/{user_id}', 'DELETE')
    
    if 'error' in result:
        await interaction.response.send_message(
            f"❌ Lỗi: {result['error']}", 
            ephemeral=True
        )
    else:
        # Xóa role
        try:
            role = interaction.guild.get_role(WHITELIST_ROLE_ID)
            if role:
                await member.remove_roles(role)
        except Exception as e:
            print(f"Error removing role: {e}")
        
        await interaction.response.send_message(
            f"✅ Đã xóa {member.mention} khỏi whitelist"
        )

@bot.tree.command(name="blacklist_add", description="Thêm user vào blacklist (chỉ admin)")
@commands.has_permissions(administrator=True)
async def blacklist_add(interaction: discord.Interaction, member: discord.Member):
    """Thêm user vào blacklist"""
    user_id = str(member.id)
    
    # Cập nhật blacklist status
    result = make_api_request(f'/whitelisted/{user_id}', 'PUT', {'blacklist': True})
    
    if 'error' in result:
        await interaction.response.send_message(
            f"❌ Lỗi: {result['error']}", 
            ephemeral=True
        )
    else:
        # Xóa role
        try:
            role = interaction.guild.get_role(WHITELIST_ROLE_ID)
            if role:
                await member.remove_roles(role)
        except Exception as e:
            print(f"Error removing role: {e}")
        
        await interaction.response.send_message(
            f"✅ Đã thêm {member.mention} vào blacklist"
        )

@bot.tree.command(name="blacklist_remove", description="Xóa user khỏi blacklist (chỉ admin)")
@commands.has_permissions(administrator=True)
async def blacklist_remove(interaction: discord.Interaction, member: discord.Member):
    """Xóa user khỏi blacklist"""
    user_id = str(member.id)
    
    # Cập nhật blacklist status
    result = make_api_request(f'/whitelisted/{user_id}', 'PUT', {'blacklist': False})
    
    if 'error' in result:
        await interaction.response.send_message(
            f"❌ Lỗi: {result['error']}", 
            ephemeral=True
        )
    else:
        await interaction.response.send_message(
            f"✅ Đã xóa {member.mention} khỏi blacklist"
        )

# ==================== CHẠY ỨNG DỤNG ====================
def run_flask():
    """Chạy Flask server trong thread riêng"""
    app.run()

def run_bot():
    """Chạy Discord bot"""
    bot.run(BOT_TOKEN)

if __name__ == '__main__':
    print("🚀 Starting Flask API + Discord Bot...")
    
    # Import requests ở đây để tránh lỗi circular import
    import requests
    
    # Chạy Flask trong thread riêng
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    print("✅ Flask API started on http://localhost:5000")
    print("🤖 Starting Discord Bot...")
    
    # Chạy Discord bot
    try:
        run_bot()
    except KeyboardInterrupt:
        print("👋 Shutting down...")
    except Exception as e:
        print(f"❌ Error: {e}")

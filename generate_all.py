# -*- coding: utf-8 -*-
"""Generate all on-brand IG post images (1080x1350) from content_plan.json into posts/."""
import json, os
from PIL import Image, ImageDraw, ImageFont
HERE=os.path.dirname(os.path.abspath(__file__))
FONT=os.path.join(HERE,"fonts","Poppins-Medium.ttf")
def F(s): return ImageFont.truetype(FONT,s)
CHAR=(22,22,22); GREEN=(0,230,118); OFFW=(244,244,242); MUTE=(154,154,149); PANEL=(35,35,32); DIM=(106,106,102)
W,H=1080,1350
def wrap(d,t,f,m):
    o=[];ln=""
    for w in t.split():
        s=(ln+" "+w).strip()
        if d.textlength(s,font=f)<=m: ln=s
        else: o.append(ln); ln=w
    if ln:o.append(ln)
    return o
def base():
    im=Image.new("RGB",(W,H),CHAR);d=ImageDraw.Draw(im)
    d.rectangle([0,0,14,H],fill=GREEN)
    tx,ty,tw,th=70,70,110,48
    d.rounded_rectangle([tx,ty,tx+tw,ty+th],radius=th//2,fill=GREEN)
    d.ellipse([tx+tw-th+6,ty+6,tx+tw-6,ty+th-6],fill=OFFW)
    d.text((tx+16,ty+14),"ON",font=F(20),fill=CHAR)
    d.text((tx+tw+18,ty+12),"MANAGER MODE ON",font=F(24),fill=OFFW)
    return im,d
def foot(d,tag):
    d.text((70,H-70),"@managermode.on",font=F(26),fill=DIM)
    d.text((W-70-d.textlength(tag,font=F(22)),H-66),tag,font=F(22),fill=DIM)
def render(p):
    t=p["type"]; im,d=base()
    if t=="before_after":
        y=360; d.text((70,y),"OFF",font=F(40),fill=MUTE)
        for i,l in enumerate(wrap(d,p["off"],F(46),W-160)): d.text((70,y+60+i*60),l,font=F(46),fill=MUTE)
        y2=720; d.text((70,y2),"ON",font=F(40),fill=GREEN)
        for i,l in enumerate(wrap(d,p["on"],F(54),W-160)): d.text((70,y2+60+i*64),l,font=F(54),fill=OFFW)
    elif t=="prompt":
        d.text((70,330),p.get("kicker","PROMPT DROP"),font=F(30),fill=GREEN)
        yy=400; y2=yy
        for i,l in enumerate(wrap(d,p["headline"],F(58),W-160)): d.text((70,yy+i*66),l,font=F(58),fill=OFFW); y2=yy+(i+1)*66
        c0=70;cy0=max(640,y2+40);c1=W-70;cy1=1150
        d.rounded_rectangle([c0,cy0,c1,cy1],radius=24,fill=PANEL); d.rectangle([c0,cy0+24,c0+8,cy1-24],fill=GREEN)
        d.text((c0+40,cy0+34),"SALIN KE AI CHAT",font=F(22),fill=GREEN)
        for i,l in enumerate(wrap(d,p["prompt"],F(34),c1-c0-90)): d.text((c0+40,cy0+90+i*46),l,font=F(34),fill=OFFW)
    else:
        yy=440; y2=yy
        for i,l in enumerate(wrap(d,p["headline"],F(66),W-150)): d.text((70,yy+i*78),l,font=F(66),fill=OFFW); y2=yy+(i+1)*78
        d.text((70,y2+40),p.get("sub","Switch ke Manager Mode: ON."),font=F(40),fill=GREEN)
    foot(d,p.get("tag",t.upper()))
    return im
if __name__=="__main__":
    plan=json.load(open(os.path.join(HERE,"content_plan.json"),encoding="utf-8"))
    os.makedirs(os.path.join(HERE,"posts"),exist_ok=True)
    for p in plan["posts"]:
        out=os.path.join(HERE,"posts",f"post-{p['id']}.png")
        render(p).save(out); print("saved",out)

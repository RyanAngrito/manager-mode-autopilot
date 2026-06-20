# -*- coding: utf-8 -*-
"""Schedule the next 3 posts (Mon/Wed/Fri 19:30 Asia/Jakarta) to Buffer using public GitHub raw image URLs.
Env required: BUFFER_TOKEN, BUFFER_CHANNEL_ID, GH_REPO (e.g. 'username/manager-mode-autopilot'). Optional: GH_BRANCH (default main)."""
import os, json, datetime, sys
from zoneinfo import ZoneInfo
import requests
HERE=os.path.dirname(os.path.abspath(__file__))
TOKEN=os.environ["BUFFER_TOKEN"]; CHANNEL=os.environ["BUFFER_CHANNEL_ID"]
REPO=os.environ["GH_REPO"]; BRANCH=os.environ.get("GH_BRANCH","main")
TZ=ZoneInfo("Asia/Jakarta")
plan=json.load(open(os.path.join(HERE,"content_plan.json"),encoding="utf-8"))["posts"]
state_path=os.path.join(HERE,"state.json")
state=json.load(open(state_path)) if os.path.exists(state_path) else {"index":0}
idx=state["index"]

def next_slots(n=3):
    """Next n occurrences of Mon(0)/Wed(2)/Fri(4) at 19:30 WIB, strictly after now."""
    now=datetime.datetime.now(TZ); slots=[]; day=now
    for _ in range(21):
        if day.weekday() in (0,2,4):
            s=day.replace(hour=19,minute=30,second=0,microsecond=0)
            if s>now: slots.append(s)
        day=day+datetime.timedelta(days=1)
        if len(slots)>=n: break
    return slots[:n]

slots=next_slots(3)
created=[]
for s in slots:
    p=plan[idx % len(plan)]; idx+=1
    img=f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/posts/post-{p['id']}.png"
    data={
      "access_token":TOKEN,
      "profile_ids[]":CHANNEL,
      "text":p["caption"],
      "media[photo]":img,
      "media[thumbnail]":img,
      "scheduled_at":s.isoformat(),
    }
    r=requests.post("https://api.bufferapp.com/1/updates/create.json",data=data,timeout=30)
    print(f"post-{p['id']} -> {s.isoformat()} : HTTP {r.status_code} {r.text[:200]}")
    if r.status_code==200: created.append(p["id"])
state["index"]=idx % len(plan)
json.dump(state,open(state_path,"w"))
print("scheduled:",created)
if not created: sys.exit("No posts scheduled — check token/channel/API response above.")

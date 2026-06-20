# Manager Mode ON — Autopilot (PC-off content engine)

Every week, in the cloud (GitHub Actions, free), this:
1. generates 8 on-brand IG posts (charcoal + green, Poppins),
2. commits them so each gets a public image URL,
3. schedules the next 3 (Mon/Wed/Fri 19:30 WIB) to your Buffer queue.

Your PC can be off. You just review/approve in the Buffer app.

## One-time setup (~15 min)

### 1. Create the repo
- Go to github.com → New repository → name it `manager-mode-autopilot` → **Public** → Create.
- On the repo page: **Add file → Upload files** → drag in EVERYTHING from this folder
  (generate_all.py, buffer_schedule.py, content_plan.json, requirements.txt, the `fonts/` folder, the `.github/` folder). Commit.

### 2. Get your Buffer token
- Open https://publish.buffer.com/settings/api and create/copy an **Access Token**.

### 3. Add secrets to the repo
- Repo → Settings → Secrets and variables → Actions → **New repository secret**. Add two:
  - `BUFFER_TOKEN` = your Buffer access token
  - `BUFFER_CHANNEL_ID` = `6a33b99538b5579345aad74e`   (this is your @managermode.on channel)

### 4. Turn it on
- Repo → **Actions** tab → enable workflows.
- Click **"Manager Mode ON - weekly autopilot" → Run workflow** to test it once now.
- After it runs, open Buffer → you should see 3 posts scheduled. Approve / move to queue.
- From then on it runs automatically every Sunday 08:00 WIB.

## Notes
- It cycles through `content_plan.json` (8 posts) — edit captions/ideas there anytime; commit, done.
- To change days/times, edit `next_slots()` in `buffer_schedule.py`.
- Buffer free plan caps ~10 scheduled posts; 3/week stays under it.
- If the Buffer step errors, check the token + that the channel ID is right (printed in the Actions log).

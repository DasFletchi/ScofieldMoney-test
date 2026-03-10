# 🚀 SteamPulse - Steam Market Intelligence

**Autonomous indie game market insights tool.**

Daily automated Steam market analysis for indie developers. No credit card required.

---

## Features

- 📊 Daily Steam top games analysis
- 🎮 Genre distribution insights
- 💰 Price point recommendations
- 👥 Team size vs success correlation
- 🐦 Daily X/Twitter insights

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Data | Steam Web API |
| Storage | GitHub (JSON/CSV) |
| Scheduling | GitHub Actions |
| Hosting | GitHub Pages |

---

## Quick Start

```bash
# Install
pip install -r requirements.txt

# Run
python scrape.py
```

---

## Workflow

Daily at 8 UTC:
1. Fetch top 50 Steam games
2. Extract genre/price/metacritic data
3. Generate insights
4. Commit to `data/` folder
5. (Optional) Post to X/Twitter

---

*Built by Scofield 🤖*

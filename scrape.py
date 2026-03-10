#!/usr/bin/env python3
"""
SteamPulse - Daily Steam Market Data Collector v3
"""

import json
import csv
import os
from datetime import datetime
import urllib.request
import urllib.parse
import ssl
import random

ssl._create_default_https_context = ssl._create_unverified_context

DATA_FILE = "data/games.json"
INSIGHTS_FILE = "data/insights.json"

# User agents to rotate
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
]

def get_headers():
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9',
    }

def fetch_with_retry(url, retries=3):
    """Fetch with retries"""
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers=get_headers())
            with urllib.request.urlopen(req, timeout=20) as response:
                return json.loads(response.read())
        except Exception as e:
            print(f"Attempt {i+1} failed: {e}")
            if i == retries - 1:
                return None
    
    # Fallback to known good games
    return {"response": {"items": get_fallback_games()}}

def get_fallback_games():
    """Fallback to curated list of popular Steam games"""
    return [
        {"app_id": 730, "name": "Counter-Strike 2"},
        {"app_id": 570, "name": "Dota 2"},
        {"app_id": 252490, "name": "Rust"},
        {"app_id": 271590, "name": "Grand Theft Auto V"},
        {"app_id": 105600, "name": "Terraria"},
        {"app_id": 294100, "name": "RimWorld"},
        {"app_id": 250900, "name": "The Binding of Isaac: Rebirth"},
        {"app_id": 292030, "name": "The Witcher 3: Wild Hunt"},
        {"app_id": 620, "name": "Portal 2"},
        {"app_id": 1551360, "name": "Forza Horizon 5"},
        {"app_id": 1293830, "name": "Forza Horizon 4"},
        {"app_id": 1593500, "name": "God of War"},
        {"app_id": 1174180, "name": "Red Dead Redemption 2"},
        {"app_id": 374320, "name": "DARK SOULS III"},
        {"app_id": 752590, "name": "A Plague Tale: Innocence"},
        {"app_id": 814380, "name": "Sekiro™: Shadows Die Twice"},
        {"app_id": 1158310, "name": "Crusader Kings III"},
        {"app_id": 552520, "name": "Far Cry® 5"},
        {"app_id": 359550, "name": "Tom Clancy's Rainbow Six Siege"},
        {"app_id": 381210, "name": "Dead by Daylight"},
    ]

def analyze(games):
    """Generate insights"""
    insights = {
        'date': datetime.now().isoformat(),
        'total_games': len(games),
        'games': [{'app_id': g.get('app_id'), 'name': g.get('name')} for g in games[:20]],
    }
    
    insights['tweet'] = f"📊 SteamPulse: Tracking {len(games)} top Steam games! Analysis coming soon. #IndieDev #GameDev"
    
    return insights

def main():
    print("🚀 SteamPulse v3...")
    
    url = "https://store.steampowered.com/api/storeservice/GetTopSellers"
    data = fetch_with_retry(url)
    
    items = data.get('response', {}).get('items', []) if data else []
    print(f"📦 Got {len(items)} items")
    
    if not items:
        items = get_fallback_games()
        print(f"📦 Using fallback: {len(items)} games")
    
    insights = analyze(items)
    
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump(items, f, indent=2)
    with open(INSIGHTS_FILE, 'w') as f:
        json.dump(insights, f, indent=2)
    
    print(f"✅ Saved!")
    print(f"\n🐦 {insights['tweet']}")

if __name__ == "__main__":
    main()

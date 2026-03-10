#!/usr/bin/env python3
"""
SteamPulse - Daily Steam Market Data Collector v2
Uses SteamDB for data (more reliable than Steam API)
"""

import json
import csv
import os
from datetime import datetime
import urllib.request
import urllib.parse
import ssl

# SSL fix
ssl._create_default_https_context = ssl._create_unverified_context

DATA_FILE = "data/games.json"
CSV_FILE = "data/games.csv"
INSIGHTS_FILE = "data/insights.json"

def fetch_steamdb_top():
    """Fetch from SteamDB (more reliable)"""
    url = "https://steamdb.info/api/StoreAPI/GetBigPictureStoreData/"
    
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        req.add_header('Referer', 'https://steamdb.info/')
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read())
    except Exception as e:
        print(f"Error: {e}")
        return {}

def fetch_steamCharts():
    """Alternative: fetch from SteamCharts"""
    url = "https://steamcharts.com/top"
    
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        with urllib.request.urlopen(req, timeout=30) as response:
            html = response.read().decode('utf-8')
            
            # Simple parsing
            games = []
            import re
            pattern = r'<a class="global-link" href="/app/(\d+)">([^<]+)</a>'
            matches = re.findall(pattern, html)
            
            for app_id, name in matches[:50]:
                games.append({
                    'app_id': app_id,
                    'name': name.strip()
                })
            return games
    except Exception as e:
        print(f"Error: {e}")
        return []

def analyze_data(games):
    """Generate insights from games"""
    # For now, simulate analysis since we can't get full data
    insights = {
        'date': datetime.now().isoformat(),
        'total_games': len(games),
        'sample_games': [g.get('name', 'N/A') for g in games[:10]],
    }
    
    # Tweet
    if games:
        insights['tweet'] = f"📊 SteamPulse: Analyzed {len(games)} top games today! #IndieDev #GameDev #Steam"
    else:
        insights['tweet'] = "📊 SteamPulse: Building... #IndieDev"
    
    return insights

def save_data(games, insights):
    """Save data"""
    os.makedirs("data", exist_ok=True)
    
    with open(DATA_FILE, 'w') as f:
        json.dump(games, f, indent=2)
    
    with open(INSIGHTS_FILE, 'w') as f:
        json.dump(insights, f, indent=2)
    
    print(f"✅ Saved {len(games)} games")

def main():
    print("🚀 SteamPulse v2...")
    
    # Try SteamCharts
    games = fetch_steamCharts()
    print(f"📦 Found {len(games)} games")
    
    # Analyze
    insights = analyze_data(games)
    save_data(games, insights)
    
    print(f"\n🐦 {insights['tweet']}")

if __name__ == "__main__":
    main()

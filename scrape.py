#!/usr/bin/env python3
"""
SteamPulse - Daily Steam Market Data Collector
Fetches top games and generates insights
"""

import json
import csv
import os
from datetime import datetime
import urllib.request
import re

DATA_FILE = "data/games.json"
CSV_FILE = "data/games.csv"
INSIGHTS_FILE = "data/insights.json"

def fetch_steam_top():
    """Fetch top selling games from Steam"""
    url = "https://store.steampowered.com/api/storeservice/GetTopSellers"
    
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0')
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read())
            return data.get('response', {}).get('items', [])
    except Exception as e:
        print(f"Error fetching Steam data: {e}")
        return []

def fetch_game_details(app_id):
    """Fetch individual game details"""
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
    
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0')
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read())
            if str(app_id) in data:
                return data[str(app_id)].get('data', {})
    except Exception as e:
        print(f"Error fetching game {app_id}: {e}")
    return {}

def clean_price(price_data):
    """Extract and normalize price"""
    if not price_data:
        return None
    final = price_data.get('final', 0)
    if final:
        return final / 100  # Convert cents to dollars
    return None

def analyze_genres(games):
    """Analyze genre distribution"""
    genre_count = {}
    genre_scores = {}
    
    for game in games:
        genres = game.get('genres', [])
        score = game.get('metacritic', 0)
        
        for genre in genres:
            name = genre.get('description', 'Unknown')
            genre_count[name] = genre_count.get(name, 0) + 1
            if score:
                if name not in genre_scores:
                    genre_scores[name] = []
                genre_scores[name].append(score)
    
    # Calculate averages
    genre_analysis = []
    for genre, count in genre_count.items():
        scores = genre_scores.get(genre, [])
        avg_score = sum(scores) / len(scores) if scores else 0
        genre_analysis.append({
            'genre': genre,
            'count': count,
            'avg_score': round(avg_score, 1)
        })
    
    return sorted(genre_analysis, key=lambda x: x['count'], reverse=True)

def generate_insights(games, genre_analysis):
    """Generate daily insights"""
    insights = {
        'date': datetime.now().isoformat(),
        'total_games': len(games),
        'top_genres': genre_analysis[:5],
        'free_to_play': len([g for g in games if g.get('price') == 0]),
        'avg_price': sum(g.get('price', 0) for g in games if g.get('price')) / max(len([g for g in games if g.get('price')]), 1),
    }
    
    # Generate tweet-ready insight
    top_genre = genre_analysis[0] if genre_analysis else {'genre': 'N/A', 'count': 0}
    insights['tweet'] = f"📊 Steam Insight: {top_genre['genre']} dominates with {top_genre['count']} titles in top 100! {insights['avg_price']:.2f}$ avg price. #IndieDev #GameDev"
    
    return insights

def save_data(games, genre_analysis, insights):
    """Save all data files"""
    os.makedirs("data", exist_ok=True)
    
    # JSON
    with open(DATA_FILE, 'w') as f:
        json.dump(games, f, indent=2)
    
    # CSV
    if games:
        with open(CSV_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'app_id', 'price', 'genres', 'metacritic', 'release_date'])
            writer.writeheader()
            for game in games:
                writer.writerow({
                    'name': game.get('name', ''),
                    'app_id': game.get('app_id', ''),
                    'price': game.get('price', ''),
                    'genres': ', '.join([g.get('description', '') for g in game.get('genres', [])]),
                    'metacritic': game.get('metacritic', ''),
                    'release_date': game.get('release_date', {}).get('date', '')
                })
    
    # Insights
    with open(INSIGHTS_FILE, 'w') as f:
        json.dump(insights, f, indent=2)
    
    print(f"✅ Saved {len(games)} games to {DATA_FILE}")
    print(f"✅ Saved insights to {INSIGHTS_FILE}")

def main():
    print("🚀 SteamPulse - Fetching data...")
    
    # Fetch top sellers
    top_items = fetch_steam_top()
    print(f"📦 Found {len(top_items)} top sellers")
    
    # Get details for each (limit to 50 for speed)
    games = []
    for item in top_items[:50]:
        app_id = item.get('app_id')
        if app_id:
            details = fetch_game_details(app_id)
            if details:
                game = {
                    'name': details.get('name'),
                    'app_id': app_id,
                    'price': clean_price(details.get('price_overview')),
                    'genres': details.get('genres', []),
                    'metacritic': details.get('metacritic', {}).get('score', 0),
                    'release_date': details.get('release_date', {}),
                    'type': details.get('type'),
                }
                games.append(game)
    
    print(f"📊 Got details for {len(games)} games")
    
    # Analyze
    genre_analysis = analyze_genres(games)
    insights = generate_insights(games, genre_analysis)
    
    # Save
    save_data(games, genre_analysis, insights)
    
    print("\n" + "="*50)
    print("📈 TOP GENRES:")
    for g in genre_analysis[:5]:
        print(f"  • {g['genre']}: {g['count']} games ({g['avg_score']}% avg)")
    print("="*50)
    print(f"\n🐦 Tweet ready:\n{insights['tweet']}")

if __name__ == "__main__":
    main()

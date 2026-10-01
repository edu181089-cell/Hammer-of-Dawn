import requests
import sqlite3
import json
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(os.path.join(BASE_DIR, 'nfl_pickem.sqlite'))
cur = conn.cursor()

# -------------------------
# DATABASE SETUP
# -------------------------
cur.execute('''CREATE TABLE IF NOT EXISTS Games (
    game_id TEXT PRIMARY KEY,
    season INTEGER,
    week INTEGER,
    home_team TEXT,
    away_team TEXT,
    home_score INTEGER,
    away_score INTEGER,
    home_win INTEGER
)''')

conn.commit()

# -------------------------
# FETCH GAMES FROM ESPN
# -------------------------
def fetch_week(season, week):
    url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?seasontype=2&week={week}&dates={season}"
    response = requests.get(url)
    data = response.json()
    return data.get('events', [])

def store_games(events, season):
    stored = 0
    for event in events:
        comp = event['competitions'][0]
        status = comp['status']['type']['state']
        if status != 'post':
            continue

        game_id = event['id']
        week = event['week']['number']

        home = next(t for t in comp['competitors'] if t['homeAway'] == 'home')
        away = next(t for t in comp['competitors'] if t['homeAway'] == 'away')

        home_team = home['team']['displayName']
        away_team = away['team']['displayName']
        home_score = int(home['score'])
        away_score = int(away['score'])
        home_win = 1 if home['winner'] else 0

        cur.execute('INSERT OR IGNORE INTO Games VALUES (?,?,?,?,?,?,?,?)',
            (game_id, season, week, home_team, away_team,
             home_score, away_score, home_win))
        stored += 1

    conn.commit()
    return stored

# Fetch 2025 full season for historical data
print("Fetching 2025 season...")
total = 0
for week in range(1, 19):
    events = fetch_week(2025, week)
    stored = store_games(events, 2025)
    print(f"  Week {week}: {stored} games stored")
    total += stored
print(f"2025 season: {total} games total")

# Fetch 2026 current season weeks 1 and 2
print("\nFetching 2026 season...")
total = 0
for week in range(1, 3):
    events = fetch_week(2026, week)
    stored = store_games(events, 2026)
    print(f"  Week {week}: {stored} games stored")
    total += stored
print(f"2026 season so far: {total} games total")

# Quick check
for row in cur.execute("SELECT season, COUNT(*) FROM Games GROUP BY season"):
    print(f"Season {row[0]}: {row[1]} games in database")
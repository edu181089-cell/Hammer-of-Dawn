import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(os.path.join(BASE_DIR, 'nfl_pickem.sqlite'))
cur = conn.cursor()

week5_picks = [
    {'home_team': 'Dallas Cowboys', 'away_team': 'Tampa Bay Buccaneers',
     'spread': -8.5, 'pick': 'Dallas Cowboys', 'confidence': 55.9},
    {'home_team': 'Jacksonville Jaguars', 'away_team': 'Philadelphia Eagles',
     'spread': -7.5, 'pick': 'Jacksonville Jaguars', 'confidence': 62.2},
    {'home_team': 'Green Bay Packers', 'away_team': 'Chicago Bears',
     'spread': 2.5, 'pick': 'Green Bay Packers', 'confidence': 81.0},
    {'home_team': 'Tennessee Titans', 'away_team': 'Houston Texans',
     'spread': 7.5, 'pick': 'Houston Texans', 'confidence': 72.9},
    {'home_team': 'Miami Dolphins', 'away_team': 'Cincinnati Bengals',
     'spread': 7.5, 'pick': 'Miami Dolphins', 'confidence': 73.1},
    {'home_team': 'New England Patriots', 'away_team': 'Las Vegas Raiders',
     'spread': -3.5, 'pick': 'New England Patriots', 'confidence': 85.0},
    {'home_team': 'New Orleans Saints', 'away_team': 'Minnesota Vikings',
     'spread': 1.5, 'pick': 'Minnesota Vikings', 'confidence': 62.2},
    {'home_team': 'New York Jets', 'away_team': 'Cleveland Browns',
     'spread': -2.5, 'pick': 'Cleveland Browns', 'confidence': 64.3},
    {'home_team': 'Pittsburgh Steelers', 'away_team': 'Indianapolis Colts',
     'spread': -2.5, 'pick': 'Indianapolis Colts', 'confidence': 59.0},
    {'home_team': 'Washington Commanders', 'away_team': 'New York Giants',
     'spread': -3.5, 'pick': 'New York Giants', 'confidence': 56.1},
    {'home_team': 'Los Angeles Chargers', 'away_team': 'Denver Broncos',
     'spread': 3.5, 'pick': 'Los Angeles Chargers', 'confidence': 57.2},
    {'home_team': 'Arizona Cardinals', 'away_team': 'Detroit Lions',
     'spread': 5.5, 'pick': 'Detroit Lions', 'confidence': 61.8},
    {'home_team': 'Seattle Seahawks', 'away_team': 'San Francisco 49ers',
     'spread': -3.0, 'pick': 'Seattle Seahawks', 'confidence': 66.7},
    {'home_team': 'Atlanta Falcons', 'away_team': 'Baltimore Ravens',
     'spread': -3.5, 'pick': 'Baltimore Ravens', 'confidence': 51.0},
    {'home_team': 'Los Angeles Rams', 'away_team': 'Buffalo Bills',
     'spread': -3.0, 'pick': 'Los Angeles Rams', 'confidence': 55.7},
]

stored = 0
for pick in week5_picks:
    cur.execute('''INSERT OR IGNORE INTO ModelPicks
        (week, season, home_team, away_team, spread, model_pick, confidence, result, correct)
        VALUES (?,?,?,?,?,?,?,?,?)''',
        (5, 2026,
         pick['home_team'],
         pick['away_team'],
         pick['spread'],
         pick['pick'],
         pick['confidence'],
         'PENDING',
         None))
    stored += 1

conn.commit()
print(f'Stored {stored} picks for Week 5')
cur.close()
conn.close()
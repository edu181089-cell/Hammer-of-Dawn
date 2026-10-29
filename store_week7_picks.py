import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(os.path.join(BASE_DIR, 'nfl_pickem.sqlite'))
cur = conn.cursor()

week7_picks = [
    {'home_team': 'Chicago Bears', 'away_team': 'New England Patriots',
     'spread': -3.0, 'pick': 'New England Patriots', 'confidence': 61.5},
    {'home_team': 'New Orleans Saints', 'away_team': 'Pittsburgh Steelers',
     'spread': 3.5, 'pick': 'Pittsburgh Steelers', 'confidence': 52.3},
    {'home_team': 'Atlanta Falcons', 'away_team': 'San Francisco 49ers',
     'spread': 3.5, 'pick': 'Atlanta Falcons', 'confidence': 51.1},
    {'home_team': 'Tennessee Titans', 'away_team': 'Cleveland Browns',
     'spread': 1.5, 'pick': 'Cleveland Browns', 'confidence': 52.7},
    {'home_team': 'Minnesota Vikings', 'away_team': 'Indianapolis Colts',
     'spread': -6.5, 'pick': 'Indianapolis Colts', 'confidence': 57.8},
    {'home_team': 'New York Jets', 'away_team': 'Miami Dolphins',
     'spread': -4.5, 'pick': 'Miami Dolphins', 'confidence': 60.6},
    {'home_team': 'Carolina Panthers', 'away_team': 'Tampa Bay Buccaneers',
     'spread': -3.5, 'pick': 'Tampa Bay Buccaneers', 'confidence': 51.7},
    {'home_team': 'Baltimore Ravens', 'away_team': 'Cincinnati Bengals',
     'spread': -2.5, 'pick': 'Baltimore Ravens', 'confidence': 53.7},
    {'home_team': 'Houston Texans', 'away_team': 'New York Giants',
     'spread': -10.0, 'pick': 'Houston Texans', 'confidence': 54.7},
    {'home_team': 'Arizona Cardinals', 'away_team': 'Denver Broncos',
     'spread': 4.5, 'pick': 'Denver Broncos', 'confidence': 61.6},
    {'home_team': 'Detroit Lions', 'away_team': 'Green Bay Packers',
     'spread': -3.0, 'pick': 'Detroit Lions', 'confidence': 57.0},
    {'home_team': 'Las Vegas Raiders', 'away_team': 'Los Angeles Rams',
     'spread': 4.5, 'pick': 'Los Angeles Rams', 'confidence': 68.3},
    {'home_team': 'Seattle Seahawks', 'away_team': 'Kansas City Chiefs',
     'spread': -2.5, 'pick': 'Seattle Seahawks', 'confidence': 65.5},
    {'home_team': 'Philadelphia Eagles', 'away_team': 'Dallas Cowboys',
     'spread': 4.5, 'pick': 'Philadelphia Eagles', 'confidence': 67.5},
]

stored = 0
for pick in week7_picks:
    cur.execute('''INSERT OR IGNORE INTO ModelPicks
        (week, season, home_team, away_team, spread, model_pick, confidence, result, correct)
        VALUES (?,?,?,?,?,?,?,?,?)''',
        (7, 2026,
         pick['home_team'],
         pick['away_team'],
         pick['spread'],
         pick['pick'],
         pick['confidence'],
         'PENDING',
         None))
    stored += 1

conn.commit()
print(f'Stored {stored} picks for Week 7')
cur.close()
conn.close()
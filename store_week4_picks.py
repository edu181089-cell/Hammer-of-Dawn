import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(os.path.join(BASE_DIR, 'nfl_pickem.sqlite'))
cur = conn.cursor()

week4_picks = [
    {'home_team': 'Cleveland Browns', 'away_team': 'Pittsburgh Steelers',
     'spread': 2.5, 'pick': 'Pittsburgh Steelers', 'confidence': 56.4},
    {'home_team': 'Washington Commanders', 'away_team': 'Indianapolis Colts',
     'spread': 3.5, 'pick': 'Indianapolis Colts', 'confidence': 57.9},
    {'home_team': 'Buffalo Bills', 'away_team': 'New England Patriots',
     'spread': -6.5, 'pick': 'New England Patriots', 'confidence': 66.9},
    {'home_team': 'Chicago Bears', 'away_team': 'New York Jets',
     'spread': -3.5, 'pick': 'Chicago Bears', 'confidence': 82.0},
    {'home_team': 'Cincinnati Bengals', 'away_team': 'Jacksonville Jaguars',
     'spread': -2.5, 'pick': 'Jacksonville Jaguars', 'confidence': 85.0},
    {'home_team': 'New York Giants', 'away_team': 'Arizona Cardinals',
     'spread': 1.5, 'pick': 'New York Giants', 'confidence': 62.0},
    {'home_team': 'Philadelphia Eagles', 'away_team': 'Los Angeles Rams',
     'spread': 3.0, 'pick': 'Los Angeles Rams', 'confidence': 56.7},
    {'home_team': 'Tampa Bay Buccaneers', 'away_team': 'Green Bay Packers',
     'spread': 3.5, 'pick': 'Green Bay Packers', 'confidence': 66.3},
    {'home_team': 'Baltimore Ravens', 'away_team': 'Tennessee Titans',
     'spread': -11.5, 'pick': 'Baltimore Ravens', 'confidence': 57.0},
    {'home_team': 'Houston Texans', 'away_team': 'Dallas Cowboys',
     'spread': -2.5, 'pick': 'Houston Texans', 'confidence': 70.9},
    {'home_team': 'Minnesota Vikings', 'away_team': 'Miami Dolphins',
     'spread': -10.5, 'pick': 'Minnesota Vikings', 'confidence': 51.0},
    {'home_team': 'Las Vegas Raiders', 'away_team': 'Kansas City Chiefs',
     'spread': 4.5, 'pick': 'Kansas City Chiefs', 'confidence': 69.5},
    {'home_team': 'San Francisco 49ers', 'away_team': 'Denver Broncos',
     'spread': -2.5, 'pick': 'San Francisco 49ers', 'confidence': 54.4},
    {'home_team': 'Seattle Seahawks', 'away_team': 'Los Angeles Chargers',
     'spread': -7.0, 'pick': 'Seattle Seahawks', 'confidence': 73.7},
    {'home_team': 'Carolina Panthers', 'away_team': 'Detroit Lions',
     'spread': 3.5, 'pick': 'Detroit Lions', 'confidence': 51.6},
    {'home_team': 'New Orleans Saints', 'away_team': 'Atlanta Falcons',
     'spread': -2.5, 'pick': 'Atlanta Falcons', 'confidence': 55.1},
]

stored = 0
for pick in week4_picks:
    cur.execute('''INSERT OR IGNORE INTO ModelPicks
        (week, season, home_team, away_team, spread, model_pick, confidence, result, correct)
        VALUES (?,?,?,?,?,?,?,?,?)''',
        (4, 2026,
         pick['home_team'],
         pick['away_team'],
         pick['spread'],
         pick['pick'],
         pick['confidence'],
         'PENDING',
         None))
    stored += 1

conn.commit()
print(f'Stored {stored} picks for Week 4')
cur.close()
conn.close()
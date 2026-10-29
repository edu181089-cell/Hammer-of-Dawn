import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(os.path.join(BASE_DIR, 'nfl_pickem.sqlite'))
cur = conn.cursor()

week6_picks = [
    {'home_team': 'Denver Broncos', 'away_team': 'Seattle Seahawks',
     'spread': 2.5, 'pick': 'Seattle Seahawks', 'confidence': 64.0},
    {'home_team': 'Jacksonville Jaguars', 'away_team': 'Houston Texans',
     'spread': -2.5, 'pick': 'Jacksonville Jaguars', 'confidence': 58.7},
    {'home_team': 'Atlanta Falcons', 'away_team': 'Chicago Bears',
     'spread': 3.0, 'pick': 'Atlanta Falcons', 'confidence': 62.3},
    {'home_team': 'Cleveland Browns', 'away_team': 'Baltimore Ravens',
     'spread': 4.5, 'pick': 'Cleveland Browns', 'confidence': 52.2},
    {'home_team': 'Indianapolis Colts', 'away_team': 'Tennessee Titans',
     'spread': -7.0, 'pick': 'Indianapolis Colts', 'confidence': 81.7},
    {'home_team': 'New England Patriots', 'away_team': 'New York Jets',
     'spread': -7.5, 'pick': 'New England Patriots', 'confidence': 85.0},
    {'home_team': 'New York Giants', 'away_team': 'New Orleans Saints',
     'spread': 1.5, 'pick': 'New York Giants', 'confidence': 66.7},
    {'home_team': 'Philadelphia Eagles', 'away_team': 'Carolina Panthers',
     'spread': -1.5, 'pick': 'Philadelphia Eagles', 'confidence': 67.5},
    {'home_team': 'Tampa Bay Buccaneers', 'away_team': 'Pittsburgh Steelers',
     'spread': 2.5, 'pick': 'Pittsburgh Steelers', 'confidence': 58.9},
    {'home_team': 'Los Angeles Rams', 'away_team': 'Arizona Cardinals',
     'spread': -12.5, 'pick': 'Los Angeles Rams', 'confidence': 69.2},
    {'home_team': 'Kansas City Chiefs', 'away_team': 'Los Angeles Chargers',
     'spread': -8.5, 'pick': 'Los Angeles Chargers', 'confidence': 58.4},
    {'home_team': 'Las Vegas Raiders', 'away_team': 'Buffalo Bills',
     'spread': 5.0, 'pick': 'Buffalo Bills', 'confidence': 81.1},
    {'home_team': 'Green Bay Packers', 'away_team': 'Dallas Cowboys',
     'spread': -1.5, 'pick': 'Green Bay Packers', 'confidence': 64.3},
    {'home_team': 'San Francisco 49ers', 'away_team': 'Washington Commanders',
     'spread': -7.5, 'pick': 'San Francisco 49ers', 'confidence': 85.0},
]

stored = 0
for pick in week6_picks:
    cur.execute('''INSERT OR IGNORE INTO ModelPicks
        (week, season, home_team, away_team, spread, model_pick, confidence, result, correct)
        VALUES (?,?,?,?,?,?,?,?,?)''',
        (6, 2026,
         pick['home_team'],
         pick['away_team'],
         pick['spread'],
         pick['pick'],
         pick['confidence'],
         'PENDING',
         None))
    stored += 1

conn.commit()
print(f'Stored {stored} picks for Week 6')
cur.close()
conn.close()
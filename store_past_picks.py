import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(os.path.join(BASE_DIR, 'nfl_pickem.sqlite'))
cur = conn.cursor()

# -------------------------
# WEEK 2 MODEL PICKS
# -------------------------
week2_picks = [
    {'home_team': 'Detroit Lions', 'away_team': 'Buffalo Bills', 
     'spread': 4.5, 'pick': 'Detroit Lions', 'confidence': 63.1},
    {'home_team': 'Atlanta Falcons', 'away_team': 'Carolina Panthers', 
     'spread': 2.5, 'pick': 'Atlanta Falcons', 'confidence': 80.7},
    {'home_team': 'Chicago Bears', 'away_team': 'Minnesota Vikings', 
     'spread': -5.5, 'pick': 'Minnesota Vikings', 'confidence': 56.4},
    {'home_team': 'Tennessee Titans', 'away_team': 'Philadelphia Eagles', 
     'spread': 7.0, 'pick': 'Philadelphia Eagles', 'confidence': 71.3},
    {'home_team': 'New York Jets', 'away_team': 'Green Bay Packers', 
     'spread': -3.5, 'pick': 'Green Bay Packers', 'confidence': 73.3},
    {'home_team': 'Tampa Bay Buccaneers', 'away_team': 'Cleveland Browns', 
     'spread': -8.5, 'pick': 'Tampa Bay Buccaneers', 'confidence': 52.0},
    {'home_team': 'Baltimore Ravens', 'away_team': 'New Orleans Saints', 
     'spread': -8.5, 'pick': 'Baltimore Ravens', 'confidence': 61.6},
    {'home_team': 'Houston Texans', 'away_team': 'Cincinnati Bengals', 
     'spread': -2.5, 'pick': 'Houston Texans', 'confidence': 76.4},
    {'home_team': 'Denver Broncos', 'away_team': 'Jacksonville Jaguars', 
     'spread': -2.5, 'pick': 'Jacksonville Jaguars', 'confidence': 85.5},
    {'home_team': 'Los Angeles Chargers', 'away_team': 'Las Vegas Raiders', 
     'spread': -6.5, 'pick': 'Los Angeles Chargers', 'confidence': 61.0},
    {'home_team': 'Dallas Cowboys', 'away_team': 'Washington Commanders', 
     'spread': -4.0, 'pick': 'Dallas Cowboys', 'confidence': 51.6},
    {'home_team': 'Arizona Cardinals', 'away_team': 'Seattle Seahawks', 
     'spread': 4.0, 'pick': 'Seattle Seahawks', 'confidence': 79.3},
    {'home_team': 'San Francisco 49ers', 'away_team': 'Miami Dolphins', 
     'spread': -13.5, 'pick': 'San Francisco 49ers', 'confidence': 59.6},
    {'home_team': 'Kansas City Chiefs', 'away_team': 'Indianapolis Colts', 
     'spread': -6.5, 'pick': 'Kansas City Chiefs', 'confidence': 54.9},
    {'home_team': 'Los Angeles Rams', 'away_team': 'New York Giants', 
     'spread': -7.5, 'pick': 'Los Angeles Rams', 'confidence': 58.8},
]

# -------------------------
# WEEK 3 MODEL PICKS
# -------------------------
week3_picks = [
    {'home_team': 'Green Bay Packers', 'away_team': 'Atlanta Falcons',
     'spread': -5.5, 'pick': 'Green Bay Packers', 'confidence': 68.1},
    {'home_team': 'Buffalo Bills', 'away_team': 'Los Angeles Chargers',
     'spread': -7.0, 'pick': 'Buffalo Bills', 'confidence': 60.7},
    {'home_team': 'Cleveland Browns', 'away_team': 'Carolina Panthers',
     'spread': 2.5, 'pick': 'Cleveland Browns', 'confidence': 53.8},
    {'home_team': 'Detroit Lions', 'away_team': 'New York Jets',
     'spread': -6.5, 'pick': 'Detroit Lions', 'confidence': 77.1},
    {'home_team': 'Indianapolis Colts', 'away_team': 'Houston Texans',
     'spread': 2.5, 'pick': 'Indianapolis Colts', 'confidence': 54.7},
    {'home_team': 'Miami Dolphins', 'away_team': 'Kansas City Chiefs',
     'spread': 11.5, 'pick': 'Miami Dolphins', 'confidence': 57.4},
    {'home_team': 'New York Giants', 'away_team': 'Tennessee Titans',
     'spread': -2.5, 'pick': 'New York Giants', 'confidence': 59.9},
    {'home_team': 'Pittsburgh Steelers', 'away_team': 'Cincinnati Bengals',
     'spread': 3.5, 'pick': 'Pittsburgh Steelers', 'confidence': 77.5},
    {'home_team': 'Washington Commanders', 'away_team': 'Seattle Seahawks',
     'spread': 7.0, 'pick': 'Seattle Seahawks', 'confidence': 82.8},
    {'home_team': 'Jacksonville Jaguars', 'away_team': 'New England Patriots',
     'spread': -3.0, 'pick': 'New England Patriots', 'confidence': 56.2},
    {'home_team': 'San Francisco 49ers', 'away_team': 'Arizona Cardinals',
     'spread': -8.5, 'pick': 'San Francisco 49ers', 'confidence': 85.0},
    {'home_team': 'Tampa Bay Buccaneers', 'away_team': 'Minnesota Vikings',
     'spread': 1.5, 'pick': 'Minnesota Vikings', 'confidence': 55.3},
    {'home_team': 'Dallas Cowboys', 'away_team': 'Baltimore Ravens',
     'spread': 3.5, 'pick': 'Dallas Cowboys', 'confidence': 55.8},
    {'home_team': 'New Orleans Saints', 'away_team': 'Las Vegas Raiders',
     'spread': -3.0, 'pick': 'New Orleans Saints', 'confidence': 62.6},
    {'home_team': 'Denver Broncos', 'away_team': 'Los Angeles Rams',
     'spread': 2.5, 'pick': 'Los Angeles Rams', 'confidence': 54.3},
    {'home_team': 'Chicago Bears', 'away_team': 'Philadelphia Eagles',
     'spread': 4.5, 'pick': 'Chicago Bears', 'confidence': 54.1},
]

def store_picks(week, season, picks):
    stored = 0
    for pick in picks:
        cur.execute('''INSERT OR IGNORE INTO ModelPicks 
            (week, season, home_team, away_team, spread, model_pick, confidence, result, correct)
            VALUES (?,?,?,?,?,?,?,?,?)''',
            (week, season,
             pick['home_team'],
             pick['away_team'],
             pick['spread'],
             pick['pick'],
             pick['confidence'],
             'PENDING',
             None))
        stored += 1
    conn.commit()
    print(f'Stored {stored} picks for Week {week}')

print('Storing past picks...')
store_picks(2, 2026, week2_picks)
store_picks(3, 2026, week3_picks)
print('Done!')

cur.close()
conn.close()
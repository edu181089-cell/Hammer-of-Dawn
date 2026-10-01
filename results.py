import requests
import sqlite3
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(os.path.join(BASE_DIR, 'nfl_pickem.sqlite'))
cur = conn.cursor()

# -------------------------
# DATABASE SETUP
# -------------------------
cur.execute('''CREATE TABLE IF NOT EXISTS ModelPicks (
    week INTEGER,
    season INTEGER,
    home_team TEXT,
    away_team TEXT,
    spread REAL,
    model_pick TEXT,
    confidence REAL,
    result TEXT,
    correct INTEGER,
    PRIMARY KEY (week, season, home_team, away_team)
)''')

cur.execute('''CREATE TABLE IF NOT EXISTS WeeklyRecord (
    week INTEGER,
    season INTEGER,
    model_correct INTEGER,
    model_total INTEGER,
    PRIMARY KEY (week, season)
)''')

conn.commit()

# -------------------------
# STORE MODEL PICKS
# -------------------------
def store_picks(week, season, picks):
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
    conn.commit()
    print(f'Stored {len(picks)} picks for Week {week}')

# -------------------------
# FETCH RESULTS AND GRADE
# -------------------------
def grade_week(week, season):
    url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?seasontype=2&week={week}&dates={season}"
    response = requests.get(url)
    data = response.json()
    events = data.get('events', [])

    graded = 0
    correct = 0

    for event in events:
        comp = event['competitions'][0]
        status = comp['status']['type']['state']
        if status != 'post':
            continue

        home = next(t for t in comp['competitors'] if t['homeAway'] == 'home')
        away = next(t for t in comp['competitors'] if t['homeAway'] == 'away')

        home_team = home['team']['displayName']
        away_team = away['team']['displayName']
        home_score = int(home['score'])
        away_score = int(away['score'])
        margin = home_score - away_score

        # Find this game in our picks
        cur.execute('''SELECT model_pick, spread FROM ModelPicks 
            WHERE week=? AND season=? AND home_team=? AND away_team=?''',
            (week, season, home_team, away_team))
        row = cur.fetchone()

        if not row:
            continue

        model_pick, spread = row

        # Grade against spread
        # spread is from home perspective (negative = home favored)
        # If home team wins by more than abs(spread) when favored = home covers
        if spread < 0:  # home team favored
            home_covered = margin > abs(spread)
            away_covered = not home_covered
        else:  # away team favored
            home_covered = margin > -spread
            away_covered = not home_covered

        if model_pick == home_team:
            is_correct = 1 if home_covered else 0
        else:
            is_correct = 1 if away_covered else 0

        result = 'WIN' if is_correct else 'LOSS'

        cur.execute('''UPDATE ModelPicks SET result=?, correct=?
            WHERE week=? AND season=? AND home_team=? AND away_team=?''',
            (result, is_correct, week, season, home_team, away_team))

        graded += 1
        correct += is_correct

        print(f"  {away_team} @ {home_team}: {away_score}-{home_score} | Pick: {model_pick} | {result}")

    conn.commit()

    if graded > 0:
        cur.execute('''INSERT OR REPLACE INTO WeeklyRecord VALUES (?,?,?,?)''',
            (week, season, correct, graded))
        conn.commit()
        print(f'\nWeek {week}: Model went {correct}-{graded-correct}')

    return correct, graded

# -------------------------
# SHOW RUNNING RECORD
# -------------------------
def show_record():
    print('\n' + '=' * 50)
    print('HAMMER OF DAWN — SEASON RECORD')
    print('=' * 50)

    total_correct = 0
    total_games = 0

    for row in cur.execute('''SELECT week, model_correct, model_total 
        FROM WeeklyRecord ORDER BY week'''):
        week, correct, total = row
        pct = round(correct/total*100, 1) if total > 0 else 0
        print(f'  Week {week}: {correct}-{total-correct} ({pct}%)')
        total_correct += correct
        total_games += total

    if total_games > 0:
        overall_pct = round(total_correct/total_games*100, 1)
        print(f'\n  OVERALL: {total_correct}-{total_games-total_correct} ({overall_pct}%)')
    print('=' * 50)

# -------------------------
# MAIN
# -------------------------
if __name__ == '__main__':
    print('HAMMER OF DAWN — Results Tracker')
    print('=' * 50)

    # Grade completed weeks
    print('\nGrading Week 2...')
    grade_week(2, 2026)

    print('\nGrading Week 3...')
    grade_week(3, 2026)

    # Show running record
    show_record()

    cur.close()
    conn.close()
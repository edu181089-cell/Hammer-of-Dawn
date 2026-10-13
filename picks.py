import sqlite3
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(os.path.join(BASE_DIR, 'nfl_pickem.sqlite'))

# -------------------------
# LOAD ALL GAMES INTO PANDAS
# -------------------------
df = pd.read_sql('SELECT * FROM Games', conn)
df['margin'] = df['home_score'] - df['away_score']

# -------------------------
# BUILD TEAM STATS
# -------------------------
def get_team_stats(team, season_filter=None):
    if season_filter:
        games = df[df['season'] == season_filter]
    else:
        games = df

    home_games = games[games['home_team'] == team]
    away_games = games[games['away_team'] == team]

    stats = {
        'games_played': len(home_games) + len(away_games),
        'avg_points_scored': pd.concat([
            home_games['home_score'],
            away_games['away_score']
        ]).mean(),
        'avg_points_allowed': pd.concat([
            home_games['away_score'],
            away_games['home_score']
        ]).mean(),
        'home_wins': home_games['home_win'].sum(),
        'home_games': len(home_games),
        'away_wins': (away_games['home_win'] == 0).sum(),
        'away_games': len(away_games),
        'avg_home_margin': home_games['margin'].mean(),
        'avg_away_margin': (-away_games['margin']).mean(),
    }
    return stats

# -------------------------
# PREDICT A GAME
# -------------------------
def predict_game(home_team, away_team, spread, public_pct_home,
                 home_qb_adj=0, away_qb_adj=0,
                 home_skill_adj=0, away_skill_adj=0):

    # Get 2025 full season stats
    home_stats = get_team_stats(home_team, 2025)
    away_stats = get_team_stats(away_team, 2025)

    # Get 2026 recent form
    home_2026 = get_team_stats(home_team, 2026)
    away_2026 = get_team_stats(away_team, 2026)

    # Base point differential
    home_diff = home_stats['avg_points_scored'] - home_stats['avg_points_allowed']
    away_diff = away_stats['avg_points_scored'] - away_stats['avg_points_allowed']

    # Home field advantage
    home_field = 2.5

    # Predicted margin
    predicted_margin = (home_diff - away_diff) + home_field

    # Recent form adjustment (2026 week 1)
    if home_2026['games_played'] > 0:
        recent_home = home_2026['avg_points_scored'] - home_2026['avg_points_allowed']
        predicted_margin += recent_home * 0.2

    if away_2026['games_played'] > 0:
        recent_away = away_2026['avg_points_scored'] - away_2026['avg_points_allowed']
        predicted_margin -= recent_away * 0.2

    # -------------------------
    # INJURY ADJUSTMENTS (NEW)
    # QB adjustments shift the predicted margin
    # Positive = helps home team, Negative = hurts home team
    # -------------------------
    predicted_margin += home_qb_adj
    predicted_margin -= away_qb_adj
    predicted_margin += home_skill_adj
    predicted_margin -= away_skill_adj

    # Public fade factor
    fade_adjustment = 0
    if public_pct_home >= 65:
        fade_adjustment = -1.0
    elif public_pct_home <= 35:
        fade_adjustment = 1.0
    predicted_margin += fade_adjustment

    # Compare to spread
    margin_vs_spread = predicted_margin - (-spread)

    if margin_vs_spread > 0:
        pick = home_team
        raw_confidence = 50 + abs(margin_vs_spread) * 3
    else:
        pick = away_team
        raw_confidence = 50 + abs(margin_vs_spread) * 3

    # -------------------------
    # LARGE SPREAD PENALTY (NEW)
    # Spreads > 7 are historically hard to cover
    # Reduce confidence on the favorite
    # -------------------------
    abs_spread = abs(spread)
    if abs_spread > 7:
        # Reduce confidence on the favored side
        favored_team = away_team if spread > 0 else home_team
        if pick == favored_team:
            penalty = (abs_spread - 7) * 2
            raw_confidence -= penalty

    confidence = min(85, max(51, raw_confidence))

    return {
        'home_team': home_team,
        'away_team': away_team,
        'spread': spread,
        'predicted_margin': round(predicted_margin, 1),
        'pick': pick,
        'confidence': round(confidence, 1),
        'public_pct_home': public_pct_home,
        'injury_notes': []
    }

# -------------------------
# WEEK 5 MATCHUPS
# Injury adjustments:
# home_qb_adj: positive helps home, negative hurts home
# away_qb_adj: positive helps away, negative hurts away
# Typical values: starter out = -7 to -9, limited = -3, questionable = -1
# -------------------------
matchups = [
    # TNF
    ('Dallas Cowboys', 'Tampa Bay Buccaneers', -8.5, 33.41,
     0, -7, 0, 0),    # Mayfield OUT

    # Sunday London
    ('Jacksonville Jaguars', 'Philadelphia Eagles', -7.5, 52.04,
     0, -1, 0, 0),    # Eagles OL retirement

    # Sunday 12pm
    ('Green Bay Packers', 'Chicago Bears', 2.5, 36.02,
     0, -9, 0, 0),    # Caleb Williams OUT — massive adjustment

    ('Tennessee Titans', 'Houston Texans', 7.5, 43.35,
     0, 0, 0, 0),

    ('Miami Dolphins', 'Cincinnati Bengals', 7.5, 30.46,
     0, 0, 0, 0),

    ('New England Patriots', 'Las Vegas Raiders', -3.5, 46.66,
     0, 0, 0, 0),

    ('New Orleans Saints', 'Minnesota Vikings', 1.5, 36.17,
     0, 0, 0, 0),

    ('New York Jets', 'Cleveland Browns', -2.5, 28.33,
     0, 0, 0, 0),

    ('Pittsburgh Steelers', 'Indianapolis Colts', -2.5, 51.71,
     0, 0, 0, 0),

    ('Washington Commanders', 'New York Giants', -3.5, 32.67,
     -3, -5, 0, 0),   # Daniels unknown + Winston starting

    ('Los Angeles Chargers', 'Denver Broncos', 3.5, 34.03,
     0, 0, 0, 0),

    ('Arizona Cardinals', 'Detroit Lions', 5.5, 33.0,
     0, 0, 0, 0),

    # Sunday 3:25pm
    ('Seattle Seahawks', 'San Francisco 49ers', -3.0, 39.0,
     0, 0, 0, 0),

    ('Atlanta Falcons', 'Baltimore Ravens', -3.5, 56.0,
     0, -6, 0, 0),    # Lamar leaning out

    # MNF
    ('Los Angeles Rams', 'Buffalo Bills', -3.0, 36.02,
     0, 0, 0, 0),
]

print('=' * 65)
print('NFL WEEK 5 2026 — MODEL PICKS (with injury adjustments)')
print('=' * 65)

results = []
for m in matchups:
    r = predict_game(*m)
    results.append(r)

    spread_val = r['spread']
    if spread_val < 0:
        spread_display = f"{r['home_team']} {spread_val}"
    else:
        spread_display = f"{r['away_team']} -{spread_val}"

    flag = ''
    if (r['public_pct_home'] >= 65 and r['pick'] == r['away_team']):
        flag = ' ⚠️  FADE THE PUBLIC'
    elif (r['public_pct_home'] <= 35 and r['pick'] == r['home_team']):
        flag = ' ⚠️  FADE THE PUBLIC'

    print(f"\n{r['away_team']} @ {r['home_team']}")
    print(f"  Spread: {spread_display}")
    print(f"  Public: {r['public_pct_home']}% on {r['home_team']}")
    print(f"  Predicted margin: Home by {r['predicted_margin']}")
    print(f"  ✅ PICK: {r['pick']} | Confidence: {r['confidence']}%{flag}")

print('\n' + '=' * 65)
print('SUMMARY — MODEL PICKS WEEK 5')
print('=' * 65)
for r in results:
    print(f"  {r['pick']}")

conn.close()
<<<<<<< HEAD
# 🔨 Hammer of Dawn — NFL Pick'em Analytics Model

> *In Gears of War, the Hammer of Dawn was the only weapon powerful enough 
> to destroy an otherwise unkillable enemy called the Berserker. After years 
> of finishing last in my pick'em league while people who don't know how many 
> players are on the field finish first — I built this.*

## What It Does

Hammer of Dawn is a data-driven NFL pick'em model that:

- Fetches live NFL game data from the ESPN public API
- Stores historical results in a SQLite database
- Calculates team performance metrics using Pandas
- Generates weekly pick recommendations against the spread
- Tracks its own performance automatically week over week

## How The Model Works

Each week the model analyzes every matchup using five factors:

1. **Point differential** — how many points a team scores vs allows on average, based on the full previous season
2. **Recent form** — how the team has performed in the current 2026 season (weighted at 20%)
3. **Home field advantage** — a 2.5 point adjustment for the home team, consistent with NFL historical data
4. **Public sentiment fade** — when 65%+ of the public picks one side, the model nudges slightly toward the other
5. **Injury adjustments** — manual QB and skill position adjustments entered weekly based on the injury report

## Spread Logic

The model predicts a margin of victory and compares it to the Vegas spread. If the predicted margin exceeds the spread, the model picks the favorite to cover. If not, it picks the underdog. Confidence starts at 50% and grows based on the gap between predicted margin and spread.

A large spread penalty reduces confidence on any team favored by more than 7 points — historically dangerous territory in the NFL.

## Current Season Record (2026)

| Week | Model | Result |
|------|-------|--------|
| 2 | 6-8 | 42.9% |
| 3 | 9-7 | 56.2% |
| **Overall** | **15-15** | **50.0%** |

*Record updates automatically each week via results.py*

## Project Structure


hammer-of-dawn/
│
├── nfl_model.py # Fetches and stores game data from ESPN API
├── picks.py # Generates weekly pick recommendations
├── results.py # Grades picks and tracks running record
├── store_past_picks.py # One-time script to seed historical picks
├── explore.py # API exploration utility
└── nfl_pickem.sqlite # SQLite database (games, picks, results)



## Technologies Used

- **Python** — data fetching, processing, and modeling
- **Pandas** — team stats calculation and data manipulation  
- **SQLite** — storing game results, picks, and performance tracking
- **ESPN Public API** — live NFL game data, no key required
- **matplotlib/seaborn** — visualization (coming soon)

## Weekly Workflow

1. Run `nfl_model.py` to fetch the latest game data
2. Check the injury report and update adjustments in `picks.py`
3. Run `picks.py` to generate the week's recommendations
4. After games complete, run `results.py` to grade and update the record

## What's Next

- Visualization dashboard showing model performance over the season
- Automated injury data fetching
- Season-end analysis comparing model vs human picks

## About

Built as a portfolio project while learning Python, SQL, and data analysis.
Part of a career transition into data analytics.

*GitHub: [github.com/edu181089-cell](https://github.com/edu181089-cell)*
=======
# Hammer-of-Dawn
NFL pick'em prediction model — data beats gut instinct (mostly)
>>>>>>> f241fd9549b5a5dcc03305d622106c44cda73249

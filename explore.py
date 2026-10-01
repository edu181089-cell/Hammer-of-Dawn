
import requests
import json

# ESPN public API - free, no key needed
# Getting NFL Week 1 2025 season scores
url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?seasontype=2&week=1&dates=2025"

print("Fetching NFL Week 1 2025 data...")
response = requests.get(url)
data = response.json()

events = data.get('events', [])
print(f"Games found: {len(events)}")

if events:
    print("\nFirst game sample:")
    print(json.dumps(events[0], indent=2))
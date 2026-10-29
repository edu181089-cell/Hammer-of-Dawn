import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(os.path.join(BASE_DIR, 'nfl_pickem.sqlite'))
cur = conn.cursor()

# Packers were the road favorite (-3.5), so the home (Jets) spread is +3.5
cur.execute("""UPDATE ModelPicks SET spread = 3.5
    WHERE week = 2 AND season = 2026
    AND home_team = 'New York Jets' AND away_team = 'Green Bay Packers'""")
print('Packers/Jets rows fixed:', cur.rowcount)

# Bills were the home team (-4.5); the row had the Lions as home
cur.execute("""UPDATE ModelPicks SET home_team = 'Buffalo Bills',
    away_team = 'Detroit Lions', spread = -4.5
    WHERE week = 2 AND season = 2026
    AND home_team = 'Detroit Lions' AND away_team = 'Buffalo Bills'""")
print('Bills/Lions rows fixed:', cur.rowcount)

conn.commit()
conn.close()
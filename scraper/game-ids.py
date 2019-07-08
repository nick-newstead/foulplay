import requests
import pandas as pd
import time
from datetime import datetime
from pathlib import Path

# Set working directory and data directory.
cwd = Path().resolve()
data = cwd.joinpath("data")

# Example URL.
# url = "https://stats.nba.com/stats/scoreboardV2?DayOffset=0&LeagueID=00&gameDate=06/12/2019"

# Header for request.
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/"
                         "537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"}

# Import previously scraped schedule to get dates of games.
# The dates will be used in the request to get Game IDs.
# This avoids unnecessary requests for days when games to not occur.
schedule = pd.read_csv(data.joinpath("nba-schedule-1999-2019.csv"))
dates = schedule["date"].unique().tolist()
dates = [datetime.strftime(datetime.strptime(date, "%Y-%m-%d"), "%m/%d/%Y") for date in dates]

# Loop through list of dates to get the IDs of games that fall on those dates.
game_ids = []
for date in dates:
  url = f"https://stats.nba.com/stats/scoreboardV2?DayOffset=0&LeagueID=00&gameDate={date}"
  response = requests.get(url, headers=headers)
  games = response.json()["resultSets"][0]["rowSet"]
  for i in range(len(games)):
    game_id = games[i][2]
    game_ids.append(game_id)
  print(date)
  time.sleep(0.5)

# Write list of game IDs to csv file.
with open(data.joinpath("game-ids.csv"), "w") as f:
  f.write("game_id\n")
  for game_id in game_ids:
    f.write(f"{game_id}\n")

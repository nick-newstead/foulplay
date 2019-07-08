import requests
import pandas as pd
import itertools
from datetime import datetime
import lxml
from pathlib import Path

# Set working directory and data directory.
cwd = Path().resolve()
data = cwd.joinpath("data")

# Example URL.
# url = "https://www.basketball-reference.com/leagues/NBA_1999_games.html"

# Header for request.
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/"
                         "537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"}

# First and last year of desired season range.
start_date = 1999
end_date = 2019

# Months when NBA games are played.
months = ["october", "november", "december", "january", "february", "march", "april", "may", "june"]

# Parse the data from the table.
def parse_game(row, playoffs=False, year=2001):
  # There is an additonal column added to the table (start time of game) for seasons after 2001.
  i = 1 if year >= 2001 else 0
  out = {"date": datetime.strptime(row[0].text_content(), "%a, %b %d, %Y"),
         "away_team": row[1+i].text_content(),
         "home_team": row[3+i].text_content(),
         "away_team_score": int(row[2+i].text_content()),
         "home_team_score": int(row[4+i].text_content()),
         "overtime": row[6+i].text_content(),
         "attendance": int(row[7+i].text_content().replace(",", "")),
         "playoff": playoffs,
         "notes": row[8+i].text_content()}
  if i == 1:
    out["start_et"] = row[1].text_content()
  return out


# Loop through specified duration of years and through each month to get the list of games for that month.
schedule = []
for year in range(start_date, end_date + 1):
  year_schedule = []
  playoffs = False
  for month in months:
    response = requests.get(f"https://www.basketball-reference.com/leagues/NBA_{year}_games-{month}.html", headers=headers)
    if response.status_code == 200:
      tree = lxml.html.fromstring(response.content)
      rows = tree.xpath("//table[@id='schedule']//tbody/tr")
      # Loop through each row in the table, each row corresponds to one game.
      # Barring one row "Playoffs" which appears before the playoff games begin.
      for row in rows:
        if row.text_content() != "Playoffs":
          year_schedule.append(parse_game(row, playoffs=playoffs, year=year))
        else:  # Set playoff signifier to True if "Playoffs row is detected".
          playoffs = True
    else:
      pass
  schedule.append(year_schedule)
schedule = list(itertools.chain.from_iterable(schedule))
schedule = pd.DataFrame(schedule).set_index("date")
schedule.to_csv(data.joinpath("nba-schedule-1999-2019.csv"))

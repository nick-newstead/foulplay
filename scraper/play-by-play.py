import requests
import pandas as pd
import itertools
import time
from pathlib import Path

# Set working directory and data directory.
cwd = Path().resolve()
data = cwd.joinpath("data")

# Test URLs.
# Play-by-play data - not sure what all the columns are.
url = "https://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2018/scores/pbp/0041800406_full_pbp.json"
# Also play-by-play data - seems to have less data than previous URL.
# url = "https://stats.nba.com/stats/playbyplayv2?EndPeriod=10&EndRange=55800&GameID=0041800406&" \
#       "RangeType=2&Season=2018-19&SeasonType=Playoffs&StartPeriod=1&StartRange=0"

# Header for request.
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/"
                         "537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"}

# Testing on *_full_pbp.json.
response = requests.get(url, headers=headers)
pbp = response.json()
# Gamecode - perhaps can be used to link back to the schedule (or maybe just use game ID)/
print(pbp["g"]["gcode"])
# List of 4 (more if OT) dictionaries for each quarter.
# "p" key is the quarter, "pd" key holds a list of the plays/events in the quarter.
# Each play/event in the list is represented by a dictionary that contains
# the (x, y) location of the event, a description, etc.
plays = pbp["g"]["pd"]
# The fourth quarter
print(plays[3]["p"])
# Dataframe of events in the first quarter.
quarter1 = pd.DataFrame(plays[0]["pla"])
# Concatenate all quarters.
game_pbp = pd.concat((pd.DataFrame(quarter["pla"]).assign(quarter=quarter["p"]) for quarter in plays))

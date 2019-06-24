from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd

# From a tutorial online (To learn, then going to work through it again by myself)
stats_list = []
for i in range(2019, 2020):
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(i) + "_per_game.html"
    html = urlopen(url)
    soup = BeautifulSoup(html)
    headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
    headers = headers[1:]
    rows = soup.findAll('tr')[1:]
    player_data = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]
    stats = pd.DataFrame(player_data, columns=headers)
    stats_list.append(stats)
    # Prints each year of stats to a csv file
    f = open("stats" + str(i) + ".csv", "w+")
    f.write(stats.to_csv())

# Next step is to go through a year, and make a new csv file for each player on each team (To be able to parse out the
# team stats and look at trends from year to year)
nba_teams = stats_list[0]
print(nba_teams['Tm'])
team_players = {}
for i in range(len(nba_teams)):
    if nba_teams['Tm'][i] in team_players.keys():
        team_players[nba_teams['Tm'][i]].append(i)
    else:
        team_players[nba_teams['Tm'][i]] = [i]
# team_players maps the teams name to the indices of every player that played for them that year
# (Indices of the dataframe)

print(team_players)
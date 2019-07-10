from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sea

# Want to be able to access the team DataFrames at any time
stats_list = []


def get_stats(start_year, end_year):
    for i in range(start_year, end_year + 1):
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
        # This is so I can build the same DataFrame in other files if I need to
        f = open("stats" + str(i) + ".csv", "w+")
        f.write(stats.to_csv())

    # Next step is to go through a year, and make a new csv file for each player on each team (To be able to parse
    # out the team stats and look at trends from year to year) team_players maps the teams name to the indices of every
    # player that played for them that year (Indices of the dataframe)
    nba_teams_2019 = stats_list[0]
    print(nba_teams_2019['Tm'])
    team_players = {}
    for i in range(len(nba_teams_2019)):
        if nba_teams_2019['Tm'][i] in team_players.keys():
            team_players[nba_teams_2019['Tm'][i]].append(i)
        else:
            team_players[nba_teams_2019['Tm'][i]] = [i]
    return team_players


# This function will create a list of each team and their cumulative stats for the year. Will not work for any
# percentage based stats. Proper input is a string like 'PTS' or 'BLK' (Any valid column name will work). Also takes a
# DataFrame for the given years team stats. The per year stats are not exact, but also allows us to see which teams
# were particularly hit by injuries or were active traders. For example, a smaller PPG total means that the team
# tinkered with their lineup less, and a high number meant that they did the opposite (Whether it be for injuries,
# strategy, or trades). This follows for any stat that you might care about.
def total_stats(col, teams_year):
    print(team_players)
    s = []
    total_points = []
    for key, value in team_players.items():
        points = 0
        t = teams_year[col]
        if key != 'TOT' and key is not None:
            print(key)
            for i in value:
                if t.loc[i] is not None:
                    points += float(t.loc[i])
            s.append((key, round(points, 3)))
            total_points.append(round(points, 3))
    print(s)
    return total_points


team_players = get_stats(2018, 2019)
blk = total_stats('BLK', stats_list[0])
pts = total_stats('PTS', stats_list[0])
plt.scatter(pts, blk)
plt.show()

# Try to do a line plot with a single players pts per game or anything as the years go on



from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd

# From a tutorial online (To learn, then going to work through it again by myself)
stats_list = []
for i in range(2000, 2019):
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(i) + "_per_game.html"
    html = urlopen(url)
    soup = BeautifulSoup(html)
    headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
    headers = headers[1:]
    rows = soup.findAll('tr')[1:]
    player_data = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]
    stats = pd.DataFrame(player_data, columns=headers)
    stats_list.append(stats)


from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd

# From a tutorial online (To learn, then going to work through it again by myself)
year = 2019
url = "https://www.basketball-reference.com/leagues/NBA_2019_per_game.html"
html = urlopen(url)
soup = BeautifulSoup(html, features="html.parser")
headers = [th.getText for th in soup.findAll('tr', limit=2)[0].findAll('th')]
headers = headers[1:]
print(headers)
rows = soup.findAll('tr')[1:]
player_stats = [[td.getText for td in rows[i].findAll('td')]for i in range(len(rows))]
stats = pd.DataFrame(player_stats, columns=headers)
print(stats.head(10))
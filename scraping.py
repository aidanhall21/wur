#%%
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import re

webpage_response = requests.get('https://www.usaultimate.org/archives/2014_club.aspx')
webpage = webpage_response.content
soup = BeautifulSoup(webpage, 'html.parser')

#%%
main_col = soup.find('div', {'id':'mainCol'})
children = main_col.findChildren('a')
all_links = [link for link in children if link.has_attr('href') == True]
event_links = [link for link in all_links if ('org/events' in link['href']) & (link['href'].find('team') == -1)]
event_links_url = [link['href'] for link in event_links]
event_links_url_std = [link + '/' if link[-1] != '/' else link for link in event_links_url]
short_links = [re.findall('https?://play.usaultimate.org/events/.*?(?=/)', link)[0] for link in event_links_url_std]
data_frames = []
#%%
errors = []
suffixes = ['/schedule/Men/Club-Men/', '/schedule/Women/Club-Women/', '/schedule/mixed/Club-Mixed/']
for link in short_links:
    for suffix in suffixes:
        try:
            webpage_response = requests.get(link + suffix)
            webpage = webpage_response.content
            soup = BeautifulSoup(webpage, 'html.parser')

            tables = soup.find_all('table')
            table_rows = soup.find_all('tr')
            heading = soup.find('div', {'class':'breadcrumbs'})
            text = []
            for child in heading.children:
                text.append(child)
            event_name = text[3].get_text()

            game_ids = []
            team_1 = []
            team_2 = []
            team_1_score = []
            team_2_score = []
            dates = []

            for row in table_rows:
                el = row.get('data-game')
                if el != None:
                    game_ids.append(el)

            for game in game_ids:
                match = soup.find('tr', {'data-game':game})
                home_team = match.find(attrs={'data-type':'game-team-home'}).get_text().replace('\n', '').split('(')
                if len(home_team) > 2:
                    team_1.append('-'.join(home_team[:-1])[:-2].replace(' -', ' ').strip())
                else:
                    team_1.append(home_team[0][:-1].strip())

                away_team = match.find(attrs={'data-type':'game-team-away'}).get_text().replace('\n', '').split('(')
                if len(away_team) > 2:
                    team_2.append('-'.join(away_team[:-1])[:-2].replace(' -', ' ').strip())
                else:
                    team_2.append(away_team[0][:-1].strip())
                #team_1.append(match.find(attrs={'data-type':'game-team-home'}).get_text().replace('\n', '').split('(')[0][:-1])
                #team_2.append(match.find(attrs={'data-type':'game-team-away'}).get_text().replace('\n', '').split('(')[0][:-1])
                team_1_score.append(match.find(attrs={'data-type':'game-score-home'}).get_text())
                team_2_score.append(match.find(attrs={'data-type':'game-score-away'}).get_text())
                raw_date = match.find(attrs={'data-type':'game-date'}).get_text()
                #### CHANGE THIS ####
                try:
                    dates.append(datetime.strptime(raw_date, '%a %m/%d').replace(year=2014).strftime('%Y-%m-%d'))
                except:
                    dates.append(datetime(2000, 1, 1))

            bracket_games = soup.select('div[id*=game]')
            for game in bracket_games:
                home_team = game.find(attrs={'data-type':'game-team-home'}).get_text().replace('\n', '').split('(')
                if len(home_team) > 2:
                    team_1.append('-'.join(home_team[:-1])[:-2].replace(' -', ' ').strip())
                else:
                    team_1.append(home_team[0][:-1].strip())

                away_team = game.find(attrs={'data-type':'game-team-away'}).get_text().replace('\n', '').split('(')
                if len(away_team) > 2:
                    team_2.append('-'.join(away_team[:-1])[:-2].replace(' -', ' ').strip())
                else:
                    team_2.append(away_team[0][:-1].strip())

                team_1_score.append(game.find(attrs={'data-type':'game-score-home'}).get_text())
                team_2_score.append(game.find(attrs={'data-type':'game-score-away'}).get_text())
                raw_date = game.find(attrs={'class':'date'}).get_text()
                try:
                    dates.append(datetime.strptime(raw_date, '%m/%d/%Y %I:%M %p').strftime('%Y-%m-%d'))
                except:
                    dates.append(datetime(2000, 1, 1))
                id = game.get('id').replace('game', '')
                game_ids.append(id)

            division = [soup.find(attrs={'class':'title'}).get_text().strip()] * len(game_ids)
            event = [event_name.strip()] * len(game_ids)

            games_dict = {'event': event, 'division':division, 'game_id':game_ids, 'team_1':team_1, 'team_1_score':team_1_score, 'team_2':team_2, 'team_2_score':team_2_score, 'game_date':dates}
            games_df = pd.DataFrame.from_dict(games_dict)
            data_frames.append(games_df)
            print('Success!')
        except Exception as ex:
            errors.append(ex)
            #print(ex)
            #print('Error: event does not exist')
            #print(link, suffix)
            #print(suffix)
            #print(short_links.index(link))

print('DONE!')
#%%
import os
season = pd.concat(data_frames)
print('Creating CSV!')
os.chdir('/Users/aidanhall/Desktop/ultimateratings/seasons')
season.to_csv('club_season_2014.csv', index=False)
print('DONE!!')

# %%
#df = []
## For single links
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import re
webpage_response = requests.get('https://play.usaultimate.org/events/Northwest-Challenge-2017/schedule/Men/CollegeMen/tier_2/')
webpage = webpage_response.content
soup = BeautifulSoup(webpage, 'html.parser')

tables = soup.find_all('table')
table_rows = soup.find_all('tr')
heading = soup.find('div', {'class':'breadcrumbs'})
text = []
for child in heading.children:
    text.append(child)
event_name = text[3].get_text()

game_ids = []
team_1 = []
team_2 = []
team_1_score = []
team_2_score = []
dates = []

for row in table_rows:
    el = row.get('data-game')
    if el != None:
        game_ids.append(el)

for game in game_ids:
    match = soup.find('tr', {'data-game':game})
    home_team = match.find(attrs={'data-type':'game-team-home'}).get_text().replace('\n', '').split('(')
    if len(home_team) > 2:
        team_1.append('-'.join(home_team[:-1])[:-2].replace(' -', ' ').strip())
    else:
        team_1.append(home_team[0][:-1].strip())

    away_team = match.find(attrs={'data-type':'game-team-away'}).get_text().replace('\n', '').split('(')
    if len(away_team) > 2:
        team_2.append('-'.join(away_team[:-1])[:-2].replace(' -', ' ').strip())
    else:
        team_2.append(away_team[0][:-1].strip())
    #team_1.append(match.find(attrs={'data-type':'game-team-home'}).get_text().replace('\n', '').split('(')[0][:-1])
    #team_2.append(match.find(attrs={'data-type':'game-team-away'}).get_text().replace('\n', '').split('(')[0][:-1])
    team_1_score.append(match.find(attrs={'data-type':'game-score-home'}).get_text())
    team_2_score.append(match.find(attrs={'data-type':'game-score-away'}).get_text())
    raw_date = match.find(attrs={'data-type':'game-date'}).get_text()
    #### CHANGE THIS ####
    dates.append(datetime.strptime(raw_date, '%a %m/%d').replace(year=2019).strftime('%Y-%m-%d'))

bracket_games = soup.select('div[id*=game]')
for game in bracket_games:
    home_team = game.find(attrs={'data-type':'game-team-home'}).get_text().replace('\n', '').split('(')
    if len(home_team) > 2:
        team_1.append('-'.join(home_team[:-1])[:-2].replace(' -', ' ').strip())
    else:
        team_1.append(home_team[0][:-1].strip())

    away_team = game.find(attrs={'data-type':'game-team-away'}).get_text().replace('\n', '').split('(')
    if len(away_team) > 2:
        team_2.append('-'.join(away_team[:-1])[:-2].replace(' -', ' ').strip())
    else:
        team_2.append(away_team[0][:-1].strip())

    team_1_score.append(game.find(attrs={'data-type':'game-score-home'}).get_text())
    team_2_score.append(game.find(attrs={'data-type':'game-score-away'}).get_text())
    raw_date = game.find(attrs={'class':'date'}).get_text()
    try:
        dates.append(datetime.strptime(raw_date, '%m/%d/%Y %I:%M %p').strftime('%Y-%m-%d'))
    except:
        dates.append(datetime(2000, 1, 1))
    id = game.get('id').replace('game', '')
    game_ids.append(id)

division = [soup.find(attrs={'class':'title'}).get_text().strip()] * len(game_ids)
event = [event_name.strip()] * len(game_ids)

games_dict = {'event': event, 'division':division, 'game_id':game_ids, 'team_1':team_1, 'team_1_score':team_1_score, 'team_2':team_2, 'team_2_score':team_2_score, 'game_date':dates}
games_df = pd.DataFrame.from_dict(games_dict)
df.append(games_df)
#data_frames.append(games_df)
print('Success!')
# %%

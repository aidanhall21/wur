#%%
import pandas as pd

## Delete duplicates, post/regular season tag, get rid of blank teams
os.chdir('/Users/aidanhall/Desktop/ultimateratings/seasons')
season = pd.read_csv('club_season_2014.csv')
season = season.drop_duplicates()
# %%
# Drop games that were not actually played
index_names = season[(season['team_1_score'] == 'W') | (season['team_1_score'] == 'L') | (season['team_1_score'] == 'F') | (season['team_2_score'] == 'W') | (season['team_2_score'] == 'L') | (season['team_2_score'] == 'F') | (season['team_1_score'] == season['team_2_score'])].index
season.drop(index_names, inplace=True)

div_split = season.division.str.split('-')
season['division'] = div_split.str.get(0).str.split(' ').str.get(0)
season['gender'] = div_split.str.get(1).str.split(' ').str.get(1)

season = season[season['team_1'].notnull()]
season = season[season['team_2'].notnull()]
# %%
# Add postseason tag
season['postseason'] = season.apply(lambda row: 1 if ((row['event'].find('Championships') != -1) | (row['event'].find('Regionals') != -1) | (row['event'].find("'s CC") != -1)) else 0, axis=1)
# %%
# Add season tag
date_split = season.game_date.str.split('-')
season['season'] = date_split.str.get(0)
print(len(season))
season.head()
# %%
#overwrite old csv
### CHANGE THIS
season.to_csv('club_season_2014.csv', index=False)
# %%
import pandas as pd
import os

years = [2014, 2015, 2016, 2017, 2018, 2019, 2020]
os.chdir('/Users/aidanhall/Desktop/ultimateratings/teams')
college_teams = pd.read_csv('college_teams.csv')
college_teams_list = list(college_teams['team'])
os.chdir('/Users/aidanhall/Desktop/ultimateratings/seasons')
teams_to_replace = []
for year in years:
    season = pd.read_csv('college_season_' + str(year) + '.csv')
    season_teams = sorted(list(set(season['team_1']) | set(season['team_2'])))
    outliers = [team for team in season_teams if team not in college_teams_list]
    not_in_dictionary = [team for team in outliers if team not in college_team_identities.keys()]
    not_replaced = [team for team in not_in_dictionary if team not in teams_to_replace]
    teams_to_replace += not_replaced

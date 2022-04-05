#%%
## add Division, Region, Conference, Wins, Losses, Rating Change, Strength of Schedule
## Scrape info from USAU ratings page
## Separate table in Database

from datetime import datetime
import pandas as pd
from collections import Counter
import numpy as np
from datetime import date
import os

os.chdir('/Users/aidanhall/Desktop/ultimateratings/seasons')

season_data = pd.read_csv('college_season_2019.csv')
prior_season_data = pd.read_csv('college_season_2018.csv')

game_data = season_data[season_data['gender'] == 'Men']
cutoff_date = datetime.date(datetime(2019, 3, 1))
start_data = datetime.date(datetime(2019, 1, 31))
game_data['datetime'] = game_data.apply(lambda row: datetime.strptime(row['game_date'], '%Y-%m-%d').date(), axis=1)
game_data = game_data[game_data['datetime'] < cutoff_date]

prior_season_game_data = prior_season_data[prior_season_data['gender'] == 'Men']
#game_data = game_data[game_data['team_1'].notnull()]
#game_data = game_data[game_data['team_2'].notnull()]
season = game_data.season.iloc[0]
#index_names = game_data[(game_data['team_1_score'] == 'W') | (game_data['team_1_score'] == 'L') | (game_data['team_1_score'] == 'F') | (game_data['team_2_score'] == 'W') | (game_data['team_2_score'] == 'L') | (game_data['team_2_score'] == 'F') | (game_data['team_1_score'] == game_data['team_2_score'])].index
#game_data.drop(index_names, inplace=True)

#game_data = pd.read_csv('college_season_2019.csv')
#game_data = game_data[game_data['gender'] == 'Men']
# Get Total Games
games_1 = game_data['team_1'].value_counts()
#games_1_prior = game_data.loc[game_data.season == (year - 1), 'team_1'].value_counts() * 0.75
games_2 = game_data['team_2'].value_counts()
#games_2_prior = game_data.loc[game_data.season == (year - 1), 'team_2'].value_counts() * 0.75
games_played = games_1.add(games_2, fill_value = 0)

game_data = pd.concat([game_data, prior_season_game_data])

teams = sorted(list(set(game_data['team_1']) | set(game_data['team_2'])))
series = pd.Series(np.zeros(len(teams)), index=teams)

total_games_current_season = games_played.add(series, fill_value=0)

game_data['team_1_score'] = pd.to_numeric(game_data['team_1_score'])
game_data['team_2_score'] = pd.to_numeric(game_data['team_2_score'])

#try:
game_data['win_A'] = game_data.apply(lambda row: 1 if ((row['team_1_score'] > row['team_2_score']) & (row['season'] == season)) else (0.6 * ((30 - total_games_current_season[row['team_1']]) / 30) if (row['team_1_score'] > row['team_2_score']) else 0), axis=1)
game_data['lose_A'] = game_data.apply(lambda row: 1 if ((row['team_1_score'] < row['team_2_score']) & (row['season'] == season)) else (0.6 * ((30 - total_games_current_season[row['team_1']]) / 30) if (row['team_1_score'] < row['team_2_score']) else 0), axis=1)

#except KeyError:
#    game_data['win_A'] = game_data.apply(lambda row: 1 if ((row['team_1_score'] > row['team_2_score']) & (row['season'] == season)) else (0.6 if (row['team_1_score'] > row['team_2_score']) else 0), axis=1)
#try:
game_data['win_B'] = game_data.apply(lambda row: 1 if ((row['team_1_score'] < row['team_2_score']) & (row['season'] == season)) else (0.6 * ((30 - total_games_current_season[row['team_2']]) / 30) if (row['team_1_score'] < row['team_2_score']) else 0), axis=1)
game_data['lose_B'] = game_data.apply(lambda row: 1 if ((row['team_1_score'] > row['team_2_score']) & (row['season'] == season)) else (0.6 * ((30 - total_games_current_season[row['team_2']]) / 30) if (row['team_1_score'] > row['team_2_score']) else 0), axis=1)

#except KeyError:
#    game_data['win_B'] = game_data.apply(lambda row: 1 if ((row['team_1_score'] < row['team_2_score']) & (row['season'] == season)) else (0.6 if (row['team_1_score'] < row['team_2_score']) else 0), axis=1)


dates = game_data['game_date']
team_A = game_data['team_1']
team_B = game_data['team_2']
win_A = game_data.win_A
lose_A = game_data.lose_A
win_B = game_data.win_B
lose_B = game_data.lose_B

d = {'date': dates, 'team_A': team_A, 'team_B': team_B, 'win_A': win_A, 'lose_A': lose_A, 'win_B': win_B, 'lose_B': lose_B}
games_df = pd.DataFrame.from_dict(d)

teams = sorted(list(set(games_df['team_A']) | set(games_df['team_B'])))

DUMMY_TEAM = 'DUMMY TEAM'
dummy_data = [[datetime(2000, 1, 1), t, DUMMY_TEAM, 1, 1, 1, 1] for t in teams]
games_df_w_dummy = pd.DataFrame(dummy_data, columns=games_df.columns)
games_df_w_dummy = pd.concat([games_df, games_df_w_dummy])

winsA = games_df_w_dummy.groupby('team_A').win_A.sum().reset_index()
winsA.drop(winsA[winsA['win_A'] == 0].index, inplace=True)
winsA.columns = ['Team', 'Wins']

winsB = games_df_w_dummy.groupby('team_B').win_B.sum().reset_index()
winsB.drop(winsB[winsB['win_B'] == 0].index, inplace=True)
winsB.columns = ['Team', 'Wins']

wins = pd.concat([winsA, winsB]).groupby('Team').Wins.sum()

num_games = Counter()
for index, row in games_df_w_dummy.iterrows():
    key1 = tuple(sorted([row['team_A'], row['team_B']]))
    if row['team_A'] == key1[0]:
        total = sum([row['win_A'], row['lose_A']])
    else:
        total = sum([row['win_B'], row['lose_B']])
    num_games[key1] += total

    key2 = tuple(sorted([row['team_A'], row['team_B']], reverse=True))
    if row['team_A'] == key2[0]:
        total = sum([row['win_A'], row['lose_A']])
    else:
        total = sum([row['win_B'], row['lose_B']])
    num_games[key2] += total

teams = sorted(list(set(games_df_w_dummy['team_A']) | set(games_df_w_dummy['team_B'])))
ratings = pd.Series(np.ones(len(teams)) / len(teams), index=teams)

max_iters = 1000
for iters in range(max_iters):
    print('iteration', iters)
    oldratings = ratings.copy()
    for team in ratings.index:
        denom = sum(num_games[tuple([team, t])] / (ratings[t] + ratings[team]) for t in ratings.index if t != team)
        ratings[team] = 1.0 * wins[team] / denom

    ratings /= sum(ratings)
    
    error = np.sum((ratings - oldratings).abs())

    if np.sum((ratings - oldratings).abs()) < 1e-4:
        break

pd.set_option('display.max_rows', None, 'display.max_columns', None)

ratings = ratings.sort_values(ascending=False)
ratings *= len(teams) # this should change maybe

### Change this for club/college
percentile = (1 - (16 / len(ratings))) * 100
value = np.percentile(ratings, percentile)
percent_ratings = pd.Series([round((rating / (rating + value)) * 100, 2) for rating in ratings], index=ratings.index)

#ratings = np.log(ratings)
ratings = round(ratings, 4)
del ratings[DUMMY_TEAM]
del percent_ratings[DUMMY_TEAM]

schedule_strength = pd.Series(np.ones(len(ratings)), index=ratings.index)

print('Calculating Strength of Schedule...')

for team in schedule_strength.index:
    team_games = sum(num_games[tuple(sorted([team, t]))] for t in schedule_strength.index if t != team)
    team_rating = sum(num_games[tuple(sorted([team, t]))] * ratings[t] for t in schedule_strength.index if t != team)
    avg_rating = float(team_rating) / team_games
    schedule_strength[team] = round(avg_rating, 2)

rank = pd.Series(range(1, len(ratings) + 1))
schedule_strength = schedule_strength.sort_values(ascending=False)
sos_rank = pd.Series(range(1, len(schedule_strength) + 1))

today = date.today().strftime('%Y-%m-%d')
dates = pd.Series([today] * len(ratings))

ratings_df = pd.DataFrame({'date':dates.values,'rank':rank.values, 'team':ratings.index, 'rating':ratings.values, 'perc_ratings':percent_ratings.values})
schedule_strength_df = pd.DataFrame({'team':schedule_strength.index, 'sos':schedule_strength.values, 'sos_rank':sos_rank.values})
final_ratings_df_2019_2 = pd.merge(ratings_df, schedule_strength_df, left_on='team', right_on='team')
#final_ratings_df.to_csv('club_mens_ratings.csv', index=False)
print('DONE!')
# %%
season_data = season_data[season_data['datetime'] < cutoff_date]
season_data = season_data[season_data['datetime'] > start_data]

game_data['rating_1'] = game_data.apply(lambda row: ratings[row['team_1']] if row['team_1'] in ratings.index else 'NA', axis=1)
game_data['rating_2'] = game_data.apply(lambda row: ratings[row['team_2']] if row['team_2'] in ratings.index else 'NA', axis=1)
index_names = game_data[(game_data['rating_1'] == 'NA') | (game_data['rating_2'] == 'NA')].index
game_data.drop(index_names, inplace=True)
game_data['fav_wpct'] = game_data.apply(lambda row: round((row['rating_1'] / (row['rating_1'] + row['rating_2'])), 2) if row['rating_1'] > row['rating_2'] else round((row['rating_2'] / (row['rating_1'] + row['rating_2'])),2), axis=1)
game_data['fav_win'] = game_data.apply(lambda row: 1 if ((row['rating_1'] > row['rating_2']) & (row['team_1_score'] > row['team_2_score'])) | ((row['rating_1'] < row['rating_2']) & (row['team_1_score'] < row['team_2_score'])) else 0, axis=1)
game_data['wpct_bucket'] = game_data.apply(lambda row: '90+' if row['fav_wpct'] >= 0.9 else ('80+' if 0.8 <= row['fav_wpct'] < 0.9 else ('70+' if 0.7 <= row['fav_wpct'] < 0.8 else ('60+' if 0.6 <= row['fav_wpct'] < 0.7 else '50+'))), axis=1)
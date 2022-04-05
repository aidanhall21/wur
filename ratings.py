#%%
## add Division, Region, Conference, Wins, Losses, Rating Change, Strength of Schedule
## Scrape info from USAU ratings page
## Separate table in Database

import pandas as pd
import os
import glob
from datetime import datetime
from collections import Counter
import numpy as np
from datetime import date

os.chdir('/Users/aidanhall/Desktop/ultimateratings/seasons')
print('In the Seasons folder')
'''
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
'''
gender = ['Mixed']
division = ['club']
years = [2019]

file = 'club_season_2019.csv'
dataframes = []
for div in division:
    for gend in gender:
        for year in years:
            try:
                season_data = pd.read_csv(file)
                game_data = season_data[season_data['gender'] == gend]
                game_data = game_data[game_data['event'] != 'USA Ultimate National Championships']
                print(game_data.head())

                # Get Total Games
                games_1 = game_data['team_1'].value_counts()
                #games_1_prior = game_data.loc[game_data.season == (year - 1), 'team_1'].value_counts() * 0.75
                games_2 = game_data['team_2'].value_counts()
                #games_2_prior = game_data.loc[game_data.season == (year - 1), 'team_2'].value_counts() * 0.75
                total_games = games_1.add(games_2, fill_value = 0)

                game_data['team_1_score'] = pd.to_numeric(game_data['team_1_score'])
                game_data['team_2_score'] = pd.to_numeric(game_data['team_2_score'])
                game_data['win_A'] = game_data.apply(lambda row: 1 if row['team_1_score'] > row['team_2_score'] else 0, axis=1)
                game_data['win_B'] = game_data.apply(lambda row: 1 if row['team_1_score'] < row['team_2_score'] else 0, axis=1)

                dates = game_data['game_date']
                team_A = game_data['team_1']
                team_B = game_data['team_2']
                win_A = game_data.win_A
                win_B = game_data.win_B

                d = {'date': dates, 'team_A': team_A, 'team_B': team_B, 'win_A': win_A, 'win_B': win_B}
                games_df = pd.DataFrame.from_dict(d)

                teams = sorted(list(set(games_df['team_A']) | set(games_df['team_B'])))

                DUMMY_TEAM = 'DUMMY TEAM'
                dummy_data = [[datetime(2000, 1, 1), t, DUMMY_TEAM, 1, 1] for t in teams]
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
                    key = tuple(sorted([row['team_A'], row['team_B']]))
                    total = sum([row['win_A'], row['win_B']])
                    num_games[key] += total

                teams = sorted(list(set(games_df_w_dummy['team_A']) | set(games_df_w_dummy['team_B'])))
                ratings = pd.Series(np.ones(len(teams)) / len(teams), index=teams)

                max_iters = 1000
                for iters in range(max_iters):
                    if iters % 25 == 0:
                        print('On iteration: ', iters)

                    oldratings = ratings.copy()
                    for team in ratings.index:
                        denom = sum(num_games[tuple(sorted([team, t]))] / (ratings[t] + ratings[team]) for t in ratings.index if t != team)
                        ratings[team] = 1.0 * wins[team] / denom

                    ratings /= sum(ratings)
                    
                    error = np.sum((ratings - oldratings).abs())
                    if iters % 25 == 0:
                        print('Error: ', error)

                    if np.sum((ratings - oldratings).abs()) < 1e-4:
                        print('Total iterations needed: ', iters)
                        print('DONE!')
                        break

                pd.set_option('display.max_rows', None, 'display.max_columns', None)

                ratings = ratings.sort_values(ascending=False)
                ratings *= len(teams) # this should change maybe

                ### Change this for club/college
                if div == 'club':
                    percentile = (1 - (16 / len(ratings))) * 100
                else:
                    percentile = (1 - (20 / len(ratings))) * 100

                value = np.percentile(ratings, percentile)
                percent_ratings = pd.Series([round((rating / (rating + value)) * 100, 1) for rating in ratings], index=ratings.index)

                ratings = np.log(ratings)
                ratings = round(ratings, 2)
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

                team_wins = []
                team_losses = []
                wpct = []

                for team in ratings.index:
                    num_wins = wins[team] - 1
                    num_losses = int(total_games[team] - num_wins)
                    team_wins.append(num_wins)
                    team_losses.append(num_losses)
                    wpct.append(round(num_wins / (num_wins + num_losses), 2))

                ratings_df = pd.DataFrame({'date':dates.values,'rank':rank.values, 'team':ratings.index, 'rating':ratings.values, 'perc_ratings':percent_ratings.values, 'wins':team_wins, 'losses':team_losses, 'w_pct':wpct})
                schedule_strength_df = pd.DataFrame({'team':schedule_strength.index, 'sos':schedule_strength.values, 'sos_rank':sos_rank.values})
                final_ratings_df = pd.merge(ratings_df, schedule_strength_df, left_on='team', right_on='team')
                final_ratings_df['division'] = [div.capitalize()] * len(final_ratings_df)
                final_ratings_df['gender'] = [gend.capitalize()] * len(final_ratings_df)
                final_ratings_df['season'] = [2019] * len(final_ratings_df)
                final_ratings_df['is_final'] = [1] * len(final_ratings_df)
                dataframes.append(final_ratings_df)
            except Exception as ex:
                print(ex)
                print(file, gend)

print('DONE!')
# %%

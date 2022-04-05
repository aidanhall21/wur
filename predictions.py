#%%
import pandas as pd
import os
import glob
from datetime import datetime
from collections import Counter
import numpy as np
from datetime import date

os.chdir('/Users/aidanhall/Desktop/ultimateratings/seasons')
print('In the Seasons folder')

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
all_filenames.remove('replacements.csv')
all_filenames.remove('temp_season.csv')

#os.chdir('/Users/aidanhall/Desktop/ultimateratings')
#print('Changed back..')
training_set = ['Regular'] # Ratings from past year full season
gender = ['Men','Women', 'Mixed']
division = ['college', 'club']
years = [2015, 2016, 2017, 2018, 2019, 2020]
tested_games = []

for div in division:
    for gend in gender:
        for el in training_set:
            for year in years:
                try:
                    '''
                    #First grab ratings from prior season full year
                    print('creating prior season ratings for:', div, gend, el, year)
                    file = div + '_season_' + str(year) + '.csv'
                    season_data = pd.read_csv(file)
                    file2 = div + '_season_' + str(year - 1) + '.csv'
                    prior_season_data = pd.read_csv(file2)

                    # Only use teams in same gender
                    game_data = prior_season_data[prior_season_data['gender'] == gend]

                    # Change scores to numeric and indicate which team won the game
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

                    print('Creating Ratings!')
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

                        if np.sum((ratings - oldratings).abs()) < 1e-4:
                            print('Total iterations needed: ', iters)
                            break

                    #pd.set_option('display.max_rows', None, 'display.max_columns', None)

                    ratings = ratings.sort_values(ascending=False)
                    ratings *= len(teams)
                    ratings = round(ratings, 4)
                    del ratings[DUMMY_TEAM]
                    '''
                    os.chdir('/Users/aidanhall/Desktop/ultimateratings/ratings')

                    ratings_file = div + '_' + gend.lower() + '_final_ratings_' + str(year - 1) + '.csv'
                    prior_season = pd.read_csv(ratings_file)
                    keys = list(prior_season['team'])
                    values = list(prior_season['rating'])

                    prior_season_final_ratings = pd.Series(values, index=keys)

                    print('Creating Ratings Based on Regular Season Games...')

                    #Ratings in each month
                    file = div + '_season_' + str(year) + '.csv'
                    os.chdir('/Users/aidanhall/Desktop/ultimateratings/seasons')
                    ratings_list = []
                    ratings_months = [1, 2, 3]
                    for month in ratings_months:
                        print('On month: ', month)
                        current_season = pd.read_csv(file)
                        current_season = current_season[current_season['gender'] == gend]
                        current_season['datetime'] = current_season.apply(lambda row: datetime.strptime(row['game_date'], '%Y-%m-%d').date(), axis=1)
                        current_season['season_month'] = current_season.datetime.apply(lambda x: 1 if ((x.month == 1) | (x.month == 6)) else (2 if ((x.month == 2) | (x.month == 7)) else (3 if ((x.month == 3) | (x.month == 8)) else 4)))
                        current_season = current_season[(current_season['season_month'] == month) | (current_season['season_month'] == month - 1) | (current_season['season_month'] == month - 2)]
                        current_season['team_1_score'] = pd.to_numeric(current_season['team_1_score'])
                        current_season['team_2_score'] = pd.to_numeric(current_season['team_2_score'])
                        current_season['win_A'] = current_season.apply(lambda row: 1 if row['team_1_score'] > row['team_2_score'] else 0, axis=1)
                        current_season['win_B'] = current_season.apply(lambda row: 1 if row['team_1_score'] < row['team_2_score'] else 0, axis=1)

                        dates = current_season['game_date']
                        team_A = current_season['team_1']
                        team_B = current_season['team_2']
                        win_A = current_season.win_A
                        win_B = current_season.win_B

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

                        print('Creating Ratings!')
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

                            if np.sum((ratings - oldratings).abs()) < 1e-4:
                                print('Total iterations needed: ', iters)
                                break

                        #pd.set_option('display.max_rows', None, 'display.max_columns', None)

                        ratings = ratings.sort_values(ascending=False)
                        ratings *= len(teams) # this should change maybe
                        ratings = round(ratings, 4)
                        del ratings[DUMMY_TEAM]
                        ratings_list.append(ratings)

                    print('Testing Regular Season Games Based on Last Years Ratings...')

                    # Test games...
                    # Only use same gender regular season games
                    season_data = pd.read_csv(file)
                    season_data = season_data[season_data['gender'] == gend]
                    season_data = season_data[season_data['postseason'] == 0]
                    season_data['datetime'] = season_data.apply(lambda row: datetime.strptime(row['game_date'], '%Y-%m-%d').date(), axis=1)
                    season_data['season_month'] = season_data.datetime.apply(lambda x: 1 if ((x.month == 1) | (x.month == 6)) else (2 if ((x.month == 2) | (x.month == 7)) else (3 if ((x.month == 3) | (x.month == 8)) else 4)))

                    game_data = season_data

                    game_data['rating_1_prior'] = game_data.apply(lambda row: prior_season_final_ratings[row['team_1']] if row['team_1'] in prior_season_final_ratings.index else 'NA', axis=1)
                    game_data['rating_2_prior'] = game_data.apply(lambda row: prior_season_final_ratings[row['team_2']] if row['team_2'] in prior_season_final_ratings.index else 'NA', axis=1)
                    game_data['ratings_1_month1'] = game_data.apply(lambda row: ratings_list[0][row['team_1']] if row['team_1'] in ratings_list[0].index else 'NA', axis=1)
                    game_data['ratings_2_month1'] = game_data.apply(lambda row: ratings_list[0][row['team_2']] if row['team_2'] in ratings_list[0].index else 'NA', axis=1)
                    game_data['ratings_1_month2'] = game_data.apply(lambda row: ratings_list[1][row['team_1']] if row['team_1'] in ratings_list[1].index else 'NA', axis=1)
                    game_data['ratings_2_month2'] = game_data.apply(lambda row: ratings_list[1][row['team_2']] if row['team_2'] in ratings_list[1].index else 'NA', axis=1)
                    game_data['ratings_1_month3'] = game_data.apply(lambda row: ratings_list[2][row['team_1']] if row['team_1'] in ratings_list[2].index else 'NA', axis=1)
                    game_data['ratings_2_month3'] = game_data.apply(lambda row: ratings_list[2][row['team_2']] if row['team_2'] in ratings_list[2].index else 'NA', axis=1)

                    index_names = game_data[(game_data['rating_1_prior'] == 'NA') | (game_data['rating_2_prior'] == 'NA')].index
                    game_data.drop(index_names, inplace=True)
                    game_data['fav_wpct'] = game_data.apply(lambda row: round((row['rating_1_prior'] / (row['rating_1_prior'] + row['rating_2_prior'])), 2) if row['rating_1_prior'] > row['rating_2_prior'] else round((row['rating_2_prior'] / (row['rating_1_prior'] + row['rating_2_prior'])),2), axis=1)
                    game_data['fav_win'] = game_data.apply(lambda row: 1 if ((row['rating_1_prior'] > row['rating_2_prior']) & (row['team_1_score'] > row['team_2_score'])) | ((row['rating_1_prior'] < row['rating_2_prior']) & (row['team_1_score'] < row['team_2_score'])) else 0, axis=1)
                    game_data['wpct_bucket'] = game_data.apply(lambda row: '90+' if row['fav_wpct'] >= 0.9 else ('80+' if 0.8 <= row['fav_wpct'] < 0.9 else ('70+' if 0.7 <= row['fav_wpct'] < 0.8 else ('60+' if 0.6 <= row['fav_wpct'] < 0.7 else '50+'))), axis=1)
                    
                    print('Games Tested...')
                    tested_games.append(game_data)

                except Exception as ex:
                    print('Error: something went wrong')
                    print(file, gend, el)
                    print(ex)
                    print('Moving on...', '\n', '\n')

print('DONE!!')            
df = pd.concat(tested_games)
os.chdir('/Users/aidanhall/Desktop/ultimateratings')
df.to_csv('predictions_file.csv', index=False)
# %%

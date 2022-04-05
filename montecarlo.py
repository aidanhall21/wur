#%%

## Import packages

import random
import numpy as np
import itertools
import math
import pandas as pd

## Input teams in tournament

nationals_teams = ['BFG', "Drag'n Thrust", 'Superlame', 'shame.', 'Seattle Mixtape', 'Space Heater', 'MOONDOG', 'Snake Country', 'Mischief', 'Toro', 'AMP', 'Polar Bears', 'Public Enemy', 'Columbus Cocktails', 'Slow White', 'Wild Card']

## Find teams in ratings dataframe (unadjusted ratings)

#nationals_teams_df = df.loc[df['team'].isin(nationals_teams)]

# %%

## Create dictionary of teams and ratings
nationals_teams_dict = {"Drag'n Thrust": 41.67910816402929,
 'Seattle Mixtape': 27.938341703236503,
 'AMP': 24.77908622458769,
 'Wild Card': 20.287399925240923,
 'Slow White': 16.281019801788425,
 'BFG': 8.004468914296352,
 'shame.': 7.76790110630677,
 'Mischief': 6.488296399286711,
 'Superlame': 6.110447432230609,
 'Toro': 5.870853361382601,
 'Snake Country': 5.812437394402588,
 'Columbus Cocktails': 4.711470182590741,
 'Space Heater': 3.8190435053663356,
 'MOONDOG': 3.7434213772608627,
 'Polar Bears': 3.189933276116184,
 'Public Enemy': 2.9446795510655237}

## Add pools

pool_a = ["Drag'n Thrust", 'Public Enemy', 'Columbus Cocktails', 'BFG']
pool_b = ['Seattle Mixtape', 'Toro', 'Space Heater', 'Polar Bears']
pool_c = ['AMP', 'Snake Country', 'Mischief', 'MOONDOG']
pool_d = ['Wild Card', 'shame.', 'Slow White', 'Superlame']

pools_list = [pool_a, pool_b, pool_c, pool_d]

# %%

## Function that chooses the winner of a game
def playMatchup(team_1, team_2, ratings_dict):
    team_1_rating = ratings_dict[team_1]
    team_2_rating = ratings_dict[team_2]

    prob_team_1_win = team_1_rating / (team_1_rating + team_2_rating)

    rand_num = random.random()

    if rand_num < prob_team_1_win:
        return team_1
    else:
        return team_2

## Function That Simulates Pool Play
def simulatePoolPlay(ratings_dict, list_of_pools):

    placements_list = []
    results_list = []
    wins_dict_list = []
    
    for pool in list_of_pools:
        wins_init = np.zeros(len(pool))
        pool_wins_dict = dict(zip(pool, wins_init))
        ## get all game combinations
        games_obj = itertools.combinations(pool, 2)
        games_list = list(games_obj)

        results = {}

        for game in games_list:
            team_1 = game[0]
            team_2 = game[1]

            winner = playMatchup(team_1, team_2, ratings_dict)

            pool_wins_dict[winner] += 1
            results[game] = winner

        win_values = sorted(list(set(pool_wins_dict.values())), reverse=True)

        team_placement = []

        ## deal with tiebreakers
        for win_total in win_values:
            teams_w_win_total = [ k for k, v in pool_wins_dict.items() if v == win_total]
            if len(teams_w_win_total) == 1:
                team_placement.append(teams_w_win_total[0])
            elif len(teams_w_win_total) == 2:
                tiebreak_winner = results[tuple(teams_w_win_total)]
                teams_w_win_total.remove(tiebreak_winner)
                tiebreak_loser = teams_w_win_total[0]
                team_placement.append(tiebreak_winner)
                team_placement.append(tiebreak_loser)
            else:
                while len(teams_w_win_total) > 0:
                    tiebreak_rand_num = random.random()
                    ind = math.floor(tiebreak_rand_num * len(teams_w_win_total))
                    team_placement.append(teams_w_win_total[ind])
                    teams_w_win_total.pop(ind)

        placements_list.append(team_placement)
        results_list.append(results)
        wins_dict_list.append(pool_wins_dict)

    return wins_dict_list, results_list, placements_list

# %%
## Simulate Pre Quarters

def simulatePreQuarters(pool_placements_list):

    ## Generate Pool Matchups

    pools = ['A', 'B', 'C', 'D']
    places = ['1', '2', '3', '4']
    pool_places_list = []
    bracket_placement_dict = {}

    for pool in pools:
        for place in places:
            pool_places_list.append(pool+place)

    i = 0
    for pool in pool_placements_list:
        for team in pool:
            bracket_placement_dict[pool_places_list[i]] = team
            i += 1

    
    matchups = [('C3', 'B2'), ('B3', 'C2'), ('A3', 'D2'), ('D3', 'A2')]
    quarters_opponents = ['A1', 'D1', 'C1', 'B1']

    ## Play Games

    winners = []

    for match in matchups:
        team_1 = bracket_placement_dict[match[0]]
        team_2 = bracket_placement_dict[match[1]]
        winning_team = playMatchup(team_1, team_2, nationals_teams_dict)
        winners.append(winning_team)

    quarters_matchups = []

    for i in range(len(winners)):

        matchup = (bracket_placement_dict[quarters_opponents[i]], winners[i])
        quarters_matchups.append(matchup)


    return winners, quarters_matchups

#%%
## Simulating Quarterfinals Through Finals

def simulateBracket(matchups_list, ratings_dict):

    semis_teams = []
    finals_teams = []

    ## Sims quarterfinals
    for game in matchups_list:
        team_1 = game[0]
        team_2 = game[1]
        winner = playMatchup(team_1, team_2, ratings_dict)
        semis_teams.append(winner)

    ## Sims Semifinals
    semi_1_winner = playMatchup(semis_teams[0], semis_teams[1], ratings_dict)
    semi_2_winner = playMatchup(semis_teams[2], semis_teams[3], ratings_dict)

    finals_teams.append(semi_1_winner)
    finals_teams.append(semi_2_winner)

    ## Sims Finals
    champion = playMatchup(finals_teams[0], finals_teams[1], ratings_dict)

    return semis_teams, finals_teams, champion

# %%

## Putting it all together

placement_df_list = []
wins_df_list = []
quarterfinals_teams_list = []
semifinals_teams_list = []
finals_teams_list = []
champions_list = []

n = 10000

for iters in range(n):

    wins_dict_list, results_list, placements_list = simulatePoolPlay(nationals_teams_dict, pools_list)

    ## creating placement dataframe
    for pool_result in placements_list:
        placement_dict = dict(zip(pool_result, list(range(1, len(pool_result) + 1))))

        df = pd.DataFrame(placement_dict, index=[iters])
        placement_df_list.append(df)

    ## creating wins dataframe
    for pool_wins_result in wins_dict_list:
        wins_df = pd.DataFrame(pool_wins_result, index=[iters])
        wins_df_list.append(wins_df)

    ## Simulating Pre Quarters
    pre_quarters_winners, quarters_matchups = simulatePreQuarters(placements_list)
    pre_quarters_byes = []
    for pool in placements_list:
        pre_quarters_byes.append(pool[0])

    quarterfinals_teams = pre_quarters_byes + pre_quarters_winners
    quarterfinals_teams_list.append(quarterfinals_teams)

    semis_teams, finals_teams, champion = simulateBracket(quarters_matchups, nationals_teams_dict)

    semifinals_teams_list.append(semis_teams)
    finals_teams_list.append(finals_teams)
    champions_list.append(champion)

#%%
## Create Round Probabilities Dictionary
placement_df = pd.concat(placement_df_list)
wins_df = pd.concat(wins_df_list)

average_place = placement_df.mean(axis=0)
average_wins = wins_df.mean(axis=0)

quarters_df = pd.DataFrame(np.array(quarterfinals_teams_list), columns=list(range(8)))
semis_df = pd.DataFrame(np.array(semifinals_teams_list), columns=list(range(4)))
finals_df = pd.DataFrame(np.array(finals_teams_list), columns=list(range(2)))

champions_series = pd.Series(champions_list)

bracket_prob_dict = {}

for pool in pools_list:
    for team in pool:
        place_counts = placement_df[team].value_counts(normalize=True)
        prob_make_bracket = round(place_counts.loc[place_counts.index < 4.0].sum() * 100, 1)
        prob_first_pool = round(place_counts.loc[place_counts.index == 1].sum() * 100, 1)
        prob_second_pool = round(place_counts.loc[place_counts.index == 2].sum() * 100, 1)
        prob_third_pool = round(place_counts.loc[place_counts.index == 3].sum() * 100, 1)
        prob_fourth_pool = round(place_counts.loc[place_counts.index == 4].sum() * 100, 1)
        prob_quarters = round((quarters_df.isin([team]).sum(axis=0).sum() / len(quarters_df)) * 100, 1)
        prob_semis = round((semis_df.isin([team]).sum(axis=0).sum() / len(semis_df)) * 100, 1)
        prob_finals = round((finals_df.isin([team]).sum(axis=0).sum() / len(finals_df)) * 100, 1)
        prob_champion = round(champions_series.value_counts(normalize=True)[team] * 100, 1)

        bracket_prob_dict[team] = {'bracket':prob_make_bracket, 'first':prob_first_pool, 'second':prob_second_pool, 'third':prob_third_pool, 'fourth':prob_fourth_pool, 'quarters':prob_quarters, 'semis':prob_semis, 'finals':prob_finals, 'champion':prob_champion}

results_dataframe = pd.DataFrame.from_dict(bracket_prob_dict)
results_dataframe = results_dataframe.T
results_dataframe = results_dataframe.sort_values(by=['champion'], ascending=False)
# %%

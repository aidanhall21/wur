#%%
## add Division, Region, Conference, Wins, Losses, Rating Change, Strength of Schedule
## Scrape info from USAU ratings page
## Separate table in Database

import pandas as pd
import os
import csv

os.chdir('/Users/aidanhall/Desktop/ultimateratings/seasons')

# %%
with open('temp_season.csv') as f:
    reader = csv.reader(f, delimiter=',')
    ### This has to be a separate file
    x = open('replacements.csv', 'w')
    for line in reader:
        if line[3] in college_team_identities.keys():
            #print('Made a change to team 1')
            #print(line)
            #print(line[3])
            print(line[3], college_team_identities[line[3]])
            line[3] = college_team_identities[line[3]]
            
        if line[5] in college_team_identities.keys():
            #print('Made a change to team 2')
            #print(line[5])
            print(line[5], college_team_identities[line[5]])
            line[5] = college_team_identities[line[5]]
        
        line = ','.join(line) + '\n'
        x.writelines(line)

x.close()

# %%
## Get rid of lines with DELETE
## Re upload to the same file
## Does the test file get overwritten or no?
os.chdir('/Users/aidanhall/Desktop/ultimateratings/seasons')
season_replaced = pd.read_csv('replacements.csv')
index_names = season_replaced[(season_replaced['team_1'] == 'DELETE') | (season_replaced['team_2'] == 'DELETE')].index
season_replaced.drop(index_names, inplace=True)
season_replaced.to_csv('college_season_2014.csv', index=False)

# %%

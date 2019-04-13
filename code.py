# --------------
import pandas as pd 
import numpy as np

# Read the data using pandas module.

#path = 'ipl_dataset.csv'
df_ipl = pd.read_csv(path)
df_ipl.shape

# Find the list of unique cities where matches were played

#df_ipl['city']
print('Unique Cities',df_ipl.loc[:,'city'].unique())

# Find the columns which contains null values if any ?
#df_ipl.isna().sum()
print('Null Values')
print(df_ipl.isnull().sum())

#how many non-null values are there?
#df_ipl.notnull().sum()


# List down top 5 most played venues

#df_ipl['venue'].value_counts().head(5)
#1. get no. of mayches played in each stadium
print('Venues details')
print(df_ipl.groupby('venue')['match_code'].nunique().sort_values(ascending=False).head(5))

# Make a runs count frequency table
print('Runs Frequency Table')
print(df_ipl['runs'].value_counts().sort_index())


# How many seasons were played and in which year they were played 
#
#df_ipl.loc[0,'date'].split('-')[0]
#df_ipl.loc[0,'date'][0:4]

#df_ipl['date'].apply(lambda x : x[0:4])
def slice_it(x):
    return x[0:4]
year = df_ipl['date'].apply(slice_it)
print(df_ipl['date'].apply(slice_it).unique())
print(df_ipl['date'].apply(slice_it).nunique())


# No. of matches played per season
df_ipl['year'] = year
print('Matches per season')
Matches_per_season = df_ipl.groupby('year')['match_code'].nunique()
print(Matches_per_season)

# Total runs across the seasons
total_runs_per_seasons = df_ipl.groupby('year')['total'].sum()
print('Total runs across the seasons')
print(total_runs_per_seasons)

# Teams who have scored more than 200+ runs. Show the top 10 results
high_scoring_teams = df_ipl.groupby(['match_code','inning','team1','team2'])['total'].sum().reset_index()
high_scoring_teams[high_scoring_teams['total']>200]
high_scoring_teams.nlargest(10,'total')

# What are the chances of chasing 200+ target
inn_1_teams = high_scoring_teams[high_scoring_teams['inning']==1]
inn_2_teams = high_scoring_teams[high_scoring_teams['inning']==2]

high_scoring = inn_1_teams.merge(inn_2_teams[['match_code','inning','total']],on='match_code')
print(high_scoring)
high_scoring['chased'] = np.where(high_scoring['total_y'] > high_scoring['total_x'],'yes','no')
chance = high_scoring['chased'].value_counts()
print(chance['yes']/(chance['yes']+chance['no'])*100)



# Which team has the highest win count in their respective seasons ?
df_ipl.drop_duplicates(subset='match_code').groupby('year')['winner'].value_counts()



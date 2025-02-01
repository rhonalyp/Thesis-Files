# Thesis-Files
Files for undergrad thesis entitled "Forecasting UAAP Women’s Volleyball Tournaments by Game Probabilities Obtained through Modified Elo Ratings"

# Optimize K 
To obtain the optimal value for the k factor, use optimizek_Elo.py for the Elo Model and optimizek_ModifiedElo.py for the Modified Elo Model. Refer to the files in the "elimination results" folder for the actual results.

# Elo Rating after the Elimination Round 
Run RatingforELoModel.py and RatingforModifiedEloModel.py to obtain the Elo Ratings for the teams in both the Elo Model and Modified Elo Model after the elimination rounds. For the needed csv files, refer to the "elimination results" folder.

# Playoffs Probabilities
To get the final four playoff probabilites, use the playoffprobabilities.py and the files in the "playoffs" folder. To Convert Elo ratings to a dictionary for quick lookups, use elo_df['Elo'] for the Elo Model, then change the 'Elo' to 'Modified Elo' for the Modified Elo Model.  The "playoffs" folder contain the 4 teams in the playoff. Since there is a difference in season 84 playoffs format, (stepladder format), run playofprobabilityladder.py instead. 

#
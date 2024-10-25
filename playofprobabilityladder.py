import pandas as pd
import numpy as np

# Read ELO ratings from CSV file
file_path = "C:/Users/rrpar/OneDrive/Desktop/Final Four Season 84.csv"
elo_df = pd.read_csv(file_path)

# Convert ELO ratings to a dictionary for quick lookups
elo = dict(zip(elo_df['Team'], elo_df['Elo']))

# Extract the teams participating in the Final Four from the CSV file
playoff_teams = list(elo.keys())


# Function to calculate the probability of one team winning a match
def match_win_probability(team_1, team_2):
    ea_1 = 1 / (1 + 10 ** ((elo[team_2] - elo[team_1]) / 400))
    ea_2 = 1- ea_1 
    return ea_1, ea_2

def best_of_three_probability(p_win_1, p_win_2):
    # Winning probabilities for Team 1
    p_win_1_2_games = p_win_1 ** 2  # Wins in 2 games
    p_win_1_3_games = p_win_1 * p_win_2 * p_win_1  # Wins in 3 games (1-0, 1-1, 2-1)

    # Winning probabilities for Team 2
    p_win_2_2_games = p_win_2 ** 2  # Wins in 2 games
    p_win_2_3_games = p_win_2 * p_win_1 * p_win_2  # Wins in 3 games (1-0, 1-1, 2-1)

    # Total probabilities
    p_series_1 = p_win_1_2_games + p_win_1_3_games  # Total probability for Team 1
    p_series_2 = p_win_2_2_games + p_win_2_3_games  # Total probability for Team 2

    return p_series_1, p_series_2
def overall_win_probabilities_stepladder(teams):
    # Step 1: Team 4 vs Team 3
    p_4_vs_3, p_3_vs_4 = match_win_probability(teams[3], teams[2])

    # Step 2: Winner of Step 1 faces Team 2
    p_2_vs_3, p_3_vs_2 = match_win_probability(teams[1], teams[2])
    p_2_vs_4, p_4_vs_2 = match_win_probability(teams[1], teams[3])

    # Step 3: Calculate conditional probabilities for the finalist
    p_2_reaches_final = (p_3_vs_4 * p_2_vs_3) + (p_4_vs_3 * p_2_vs_4)
    p_3_reaches_final = p_3_vs_4 * p_2_vs_3
    p_4_reaches_final = p_4_vs_3 * p_2_vs_4

    # Step 4: Finals (Best-of-Three) with Team 1
    p_1_vs_2, p_2_vs_1 = best_of_three_probability(match_win_probability(teams[0],teams[2])[0], p_2_reaches_final)
    p_1_vs_3, p_3_vs_1 = best_of_three_probability(match_win_probability(teams[0],teams[2])[0], p_3_reaches_final)
    p_1_vs_4, p_4_vs_1 = best_of_three_probability(match_win_probability(teams[0],teams[2])[0], p_4_reaches_final)

    # Calculate overall tournament win probabilities using conditional outcomes
    prob_team_1_wins = (
        p_2_reaches_final * p_1_vs_2 +
        p_3_reaches_final * p_1_vs_3 +
        p_4_reaches_final * p_1_vs_4
    )
    prob_team_2_wins = p_2_reaches_final * p_2_vs_1
    prob_team_3_wins = p_3_reaches_final * p_3_vs_1
    prob_team_4_wins = p_4_reaches_final * p_4_vs_1

    # Display the results
    print("\nOverall Tournament Win Probabilities:")
    print(f"{teams[0]}: {prob_team_1_wins:.4f}")
    print(f"{teams[1]}: {prob_team_2_wins:.4f}")
    print(f"{teams[2]}: {prob_team_3_wins:.4f}")
    print(f"{teams[3]}: {prob_team_4_wins:.4f}")

# Run the tournament simulation with the input CSV data
overall_win_probabilities_stepladder(playoff_teams)

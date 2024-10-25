import pandas as pd
import numpy as np

# Read ELO ratings from CSV file
file_path = "C:/Users/rrpar/OneDrive/Desktop/Final Four Season 85.csv"
elo_df = pd.read_csv(file_path)

# Convert ELO ratings to a dictionary for quick lookups
elo = dict(zip(elo_df['Team'], elo_df['Elo']))

# Extract the teams participating in the Final Four from the CSV file
playoff_teams = list(elo.keys())


# Function to calculate the probability of one team winning a match
def match_win_probability(team_1, team_2):
    ea_1 = 1 / (1 + 10 ** ((elo[team_2] - elo[team_1]) / 400))
    ea_2 = 1 / (1 + 10 ** ((elo[team_1] - elo[team_2]) / 400)) 
    return ea_1, ea_2

def best_of_three_probability(team_1, team_2):
    p_win_1, p_win_2 = match_win_probability(team_1, team_2)
    p_series_1 = (p_win_1 ** 2) * (3 - 2 * p_win_1)
    p_series_2 = (p_win_2 ** 2) * (3 - 2 * p_win_2)
    return p_series_1, p_series_2

# Function to calculate twice-to-beat probabilities
def twice_to_beat_probability(higher_seed, lower_seed):
    p1, p2 = match_win_probability(higher_seed, lower_seed)
    prob_higher_advances = p1 + p2 * p1
    prob_lower_advances = p2 * p2
    return prob_higher_advances, prob_lower_advances

# Function to calculate overall tournament win probabilities
def overall_win_probabilities(teams):
    # Semifinal probabilities (twice-to-beat format)
    prob_1_adv, prob_4_adv = twice_to_beat_probability(teams[0], teams[3])  # 1st vs 4th seed
    prob_2_adv, prob_3_adv = twice_to_beat_probability(teams[1], teams[2])  # 2nd vs 3rd seed

    # Finals probabilities (best-of-three format)
    p_1_vs_2, p_2_vs_1 = best_of_three_probability(teams[0], teams[1])
    p_1_vs_3, p_3_vs_1 = best_of_three_probability(teams[0], teams[2])
    p_4_vs_2, p_2_vs_4 = best_of_three_probability(teams[3], teams[1])
    p_4_vs_3, p_3_vs_4 = best_of_three_probability(teams[3], teams[2])

    # Calculate overall tournament win probabilities
    prob_team_1_wins = prob_1_adv * (prob_2_adv * p_1_vs_2 + prob_3_adv * p_1_vs_3)
    prob_team_2_wins = prob_2_adv * (prob_1_adv * p_2_vs_1 + prob_4_adv * p_2_vs_4)
    prob_team_3_wins = prob_3_adv * (prob_1_adv * p_3_vs_1 + prob_4_adv * p_3_vs_4)
    prob_team_4_wins = prob_4_adv * (prob_2_adv * p_4_vs_2 + prob_3_adv * p_4_vs_3)

    # Display the results
    print("\nOverall Tournament Win Probabilities:")
    print(f"{teams[0]}: {prob_team_1_wins:.4f}")
    print(f"{teams[1]}: {prob_team_2_wins:.4f}")
    print(f"{teams[2]}: {prob_team_3_wins:.4f}")
    print(f"{teams[3]}: {prob_team_4_wins:.4f}")

# Run the tournament simulation with the input CSV data
overall_win_probabilities(playoff_teams)


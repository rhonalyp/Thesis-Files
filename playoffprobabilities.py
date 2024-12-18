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
    ea_2 = 1-ea_1
    return ea_1, ea_2

def best_of_three_probability(team1,team2):
    p_win_1,p_win_2= match_win_probability(team1,team2) 
    # Winning probabilities for Team 1
    p_win_1_2_games = p_win_1 ** 2  # Wins in 2 games
    p_win_1_3_games = 2*(p_win_1 * p_win_2 * p_win_1)  # Wins in 3 games (1-0, 1-1, 2-1)

    # Winning probabilities for Team 2
    p_win_2_2_games = p_win_2 ** 2  # Wins in 2 games
    p_win_2_3_games = 2*(p_win_2 * p_win_1 * p_win_2)  # Wins in 3 games (1-0, 1-1, 2-1)

    # Total probabilities
    p_series_1 = p_win_1_2_games + p_win_1_3_games  # Total probability for Team 1
    p_series_2 = p_win_2_2_games + p_win_2_3_games  # Total probability for Team 2

    return p_series_1, p_series_2

# Function to calculate twice-to-beat probabilities
def twice_to_beat_probability(higher_seed, lower_seed):
    p1, p2 = match_win_probability(higher_seed, lower_seed)
    prob_higher_advances= p1+p2*p1
    prob_lower_advances = p2 * p2
    return prob_higher_advances, prob_lower_advances

# Function to calculate overall tournament win probabilities
def overall_win_probabilities(teams):
    # Semifinal probabilities (twice-to-beat format)
    prob_1_adv, prob_4_adv = twice_to_beat_probability(teams[0], teams[3])  # 1st vs 4th seed
    prob_2_adv, prob_3_adv = twice_to_beat_probability(teams[1], teams[2])  # 2nd vs 3rd seed

    # Finals probabilities (best-of-three format)
    p_1_vs_2, p_2_vs_1 = best_of_three_probability(teams[0],teams[1])
    p_1_vs_3, p_3_vs_1 = best_of_three_probability(teams[1],teams[2])
    p_4_vs_2, p_2_vs_4 = best_of_three_probability(teams[2],teams[3])
    p_4_vs_3, p_3_vs_4 = best_of_three_probability(teams[3],teams[3])

    # Calculate overall tournament win probabilities
    prob_team_1_wins = prob_1_adv * (prob_2_adv * p_1_vs_2 + prob_3_adv * p_1_vs_3)
    prob_team_2_wins = prob_2_adv * (prob_1_adv * p_2_vs_1 + prob_4_adv * p_2_vs_4)
    prob_team_3_wins = prob_3_adv * (prob_1_adv * p_3_vs_1 + prob_4_adv * p_3_vs_4)
    prob_team_4_wins = prob_4_adv * (prob_2_adv * p_4_vs_2 + prob_3_adv * p_4_vs_3)

   # Store probabilities in a dictionary for sorting
    tournament_probs = {
        teams[0]: prob_team_1_wins,
        teams[1]: prob_team_2_wins,
        teams[2]: prob_team_3_wins,
        teams[3]: prob_team_4_wins
    }

    # Sort teams by their tournament win probabilities in descending order
    sorted_probs = sorted(tournament_probs.items(), key=lambda x: x[1], reverse=True)
    print("Semifinals Probabilities:")
    print(f"{teams[0]}: {prob_1_adv:.4f}")
    print(f"{teams[3]}: {prob_4_adv:.4f}")
    print(f"{teams[1]}: {prob_2_adv:.4f}")
    print(f"{teams[2]}: {prob_3_adv:.4f}")

    # Possible Finals Match 
    print("Possible Finals Match")
    print(f"{teams[0]} vs {teams[1]}: {p_1_vs_2:.4f}, {p_2_vs_1:.4f}")
    print(f"{teams[0]} vs {teams[2]}: {p_1_vs_3:.4f}, {p_3_vs_1:.4f}")
    print(f"{teams[1]} vs {teams[3]}: {p_2_vs_4:.4f}, {p_4_vs_2:.4f}")
    print(f"{teams[2]} vs {teams[3]}: {p_3_vs_4:.4f}, {p_4_vs_3:.4f}")
    # Display the sorted overall tournament win probabilities
    print("\nOverall Tournament Win Probabilities (Highest to Lowest):")
    for team, prob in sorted_probs:
        print(f"{team}: {prob:.4f}")

# Run the tournament simulation with the input CSV data
overall_win_probabilities(playoff_teams)


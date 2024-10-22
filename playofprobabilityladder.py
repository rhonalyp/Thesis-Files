import pandas as pd
import numpy as np

# Read ELO ratings from CSV file
file_path = "C:/Users/rrpar/OneDrive/Desktop/Final Four Season 84.csv" #change csvv file per season
elo_df = pd.read_csv(file_path)

# Convert ELO ratings to a dictionary for quick lookups
elo = dict(zip(elo_df['Team'], elo_df['Elo']))

# Initialize dictionaries to track sets won and total sets played
sets_won = {team: 0 for team in elo}
total_sets_played = {team: 0 for team in elo}

# ELO adjustment factor (K-value)
K = 50  

# Extract the teams participating in the Final Four from the CSV file
playoff_teams = list(elo.keys())

# Function to calculate ELO-based win probabilities for both teams
def calculate_probabilities(team_1, team_2):
    ea_1 = 1 / (1 + 10 ** ((elo[team_2] - elo[team_1]) / 400))
    ea_2 = 1 - ea_1  # Complementary probability
    return ea_1, ea_2

# Function to simulate a match and update ELO ratings
def simulate_match(team_1, team_2):
    num_sets = np.random.randint(3, 6)  # Random number of sets (3 to 5)

    sets_won_team1, sets_won_team2 = 0, 0
    for _ in range(num_sets):
        ea_1, ea_2 = calculate_probabilities(team_1, team_2)
        outcome = np.random.random()

        if outcome < ea_1:
            sets_won_team1 += 1
        else:
            sets_won_team2 += 1

    # Update set statistics
    sets_won[team_1] += sets_won_team1
    sets_won[team_2] += sets_won_team2
    total_sets_played[team_1] += num_sets
    total_sets_played[team_2] += num_sets

    # Use SA as the outcome for ELO update
    sa_1 = sets_won_team1 / num_sets 
    sa_2 = sets_won_team2 / num_sets 
    update_elo(team_1, team_2, sa_1, sa_2)

    print(f"[MATCH] {team_1} vs {team_2}:")
    print(f"  Probabilities: {team_1}: {ea_1:.2f}, {team_2}: {ea_2:.2f}")
    
    return team_1 if sets_won_team1 > sets_won_team2 else team_2

# Function to update ELO ratings using SA
def update_elo(team_1, team_2, sa_1, sa_2):
    ea_1, ea_2 = calculate_probabilities(team_1, team_2)

    elo[team_1] += K * (sa_1 - ea_1)
    elo[team_2] += K * (sa_2 - ea_2)

# Function to simulate a twice-to-beat playoff round
def twice_to_beat(higher_seed, lower_seed):
    first_winner = simulate_match(higher_seed, lower_seed)
    if first_winner == higher_seed:
        return higher_seed
    else:
        second_winner = simulate_match(higher_seed, lower_seed)
        return lower_seed if second_winner == lower_seed else higher_seed

# Stepladder playoff logic
def stepladder_playoffs(teams):
    # Third seed (#3) vs Fourth seed (#4) – Single match elimination
    print("\n[STEP LADDER ROUND] Third Seed (#3) vs Fourth Seed (#4):")
    semifinalist = simulate_match(teams[2], teams[3])

    # Winner of step ladder faces the second seed (#2) – Twice to beat
    print("\n[STEP LADDER ROUND] Winner vs Second Seed (#2):")
    finalist = twice_to_beat(teams[1], semifinalist)

    # Finalist faces the top seed (#1) in the finals
    print("\n[FINALS] Top Seed (#1) vs Winner of Step Ladder:")
    champion = simulate_match(teams[0], finalist)

    return champion

# Function to display final win probabilities and updated ELO ratings
def display_final_probabilities_and_elo(teams):
    print("\nFinal Win Probabilities and Updated ELO Ratings:")
    for team in teams:
        for opponent in teams:
            if team != opponent:
                ea, _ = calculate_probabilities(team, opponent)
                print(f"{team} vs {opponent}: Win Probability = {ea:.2f}")
        print(f"{team}: Final ELO = {elo[team]:.2f}")

# Simulate the stepladder playoff format
elo = dict(zip(elo_df['Team'], elo_df['Elo']))  # Reset ELO ratings
champion = stepladder_playoffs(playoff_teams)

# Display the champion
print(f"\nChampion: {champion}")

# Display final probabilities and updated ELO ratings
display_final_probabilities_and_elo(playoff_teams)

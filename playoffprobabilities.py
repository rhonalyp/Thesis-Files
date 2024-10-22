import pandas as pd
import numpy as np

# Read ELO ratings from CSV file
file_path = "C:/Users/rrpar/OneDrive/Desktop/Final Four Season 85.csv"
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

    print(f"[SEMIFINAL] {team_1} vs {team_2}:")
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

# Function to simulate a best-of-three series for the finals
def best_of_three(team_1, team_2):
    wins_team1, wins_team2 = 0, 0

    # Play up to 3 matches
    for _ in range(3):
        winner = simulate_match(team_1, team_2)
        if winner == team_1:
            wins_team1 += 1
        else:
            wins_team2 += 1

        # Check if any team wins 2 matches (series won)
        if wins_team1 == 2:
            return team_1
        elif wins_team2 == 2:
            return team_2

# Function to determine the champion based on win probabilities
def determine_champion_by_probability(team_1, team_2):
    ea_1, ea_2 = calculate_probabilities(team_1, team_2)
    print(f"\nFinals: {team_1} Win Probability = {ea_1:.2f}, {team_2} Win Probability = {ea_2:.2f}")

    champion = team_1 if ea_1 > ea_2 else team_2
    print(f"Champion (Highest Probability): {champion}")
    return champion

# Function to simulate the playoffs
def simulate_playoffs(teams):
    finalist1 = twice_to_beat(teams[0], teams[3])  # 1st vs 4th seed
    finalist2 = twice_to_beat(teams[1], teams[2])  # 2nd vs 3rd seed

    # Determine the champion based on win probabilities
    champion = determine_champion_by_probability(finalist1, finalist2)
    return champion

# Run the playoff simulation and update ELO ratings
elo = dict(zip(elo_df['Team'], elo_df['Elo']))  # Reset ELO ratings
champion = simulate_playoffs(playoff_teams)

# Display the champion
print(f"\nChampion: {champion}")

# Display final probabilities and updated ELO ratings
print("\nFinal Win Probabilities and Updated ELO Ratings:")
for team in playoff_teams:
    for opponent in playoff_teams:
        if team != opponent:
            ea, _ = calculate_probabilities(team, opponent)
            print(f"{team} vs {opponent}: Win Probability = {ea:.2f}")
    print(f"{team}: Final ELO = {elo[team]:.2f}")

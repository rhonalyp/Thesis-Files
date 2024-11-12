import pandas as pd

# Function to calculate ELO rating
def get_elo(i):
    # Retrieve teams and sets won from the DataFrame
    team_1 = df.iloc[i]['team1']
    team_2 = df.iloc[i]['team2']
    setswon1 = df.iloc[i]['setswon1']
    setswon2 = df.iloc[i]['setswon2']

    # Calculate match outcome as a fraction (S_1 and S_2)
    total_sets = setswon1 + setswon2
    S_1 = setswon1 / total_sets
    S_2 = setswon2 / total_sets

    # ELO expected scores
    ea_1 = 1 / (1 + 10 ** ((elo[team_2] - elo[team_1]) / 400))
    ea_2 = 1-ea_1
    # ELO adjustment factor (K-value)
    k = 184

    # Update ELO ratings
    elo[team_1] += k * (S_1 - ea_1)
    elo[team_2] += k * (S_2 - ea_2)

    # Print current ELO ratings of the opposing teams
    print(f"After match {i + 1} ({team_1} vs {team_2}):")
    print(f"  {team_1}: ELO = {round(elo[team_1], 4)}")
    print(f"  {team_1}: EA = {round(ea_1, 4)}")
    print(f"  {team_2}: ELO = {round(elo[team_2], 4)}\n")
    print(f"  {team_2}: EA = {round(ea_2, 4)}")

# File path to the CSV
file_path = r"C:/Users/rrpar/OneDrive/Desktop/UAAP WVB Eliminations/Season 84 Eliminations.csv"

# Read the CSV with proper encoding handling
df = pd.read_csv(file_path, encoding='ISO-8859-1')
df.dropna(how='all', axis=1, inplace=True)  # Remove empty columns

# Initialize ELO ratings dictionary with all teams set to 1500
teams = pd.concat([df['team1'], df['team2']]).unique()
elo = {team: 1500 for team in teams}

# Calculate ELO ratings for each game in the dataset
for i in range(len(df)):
    get_elo(i)

# Print final ELO ratings for all teams
print("Final ELO Ratings:")
for team, rating in sorted(elo.items(), key=lambda x: x[1], reverse=True):
    print(f"{team}: ELO = {round(rating, 4)}")
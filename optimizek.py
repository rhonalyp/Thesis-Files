import pandas as pd

# Function to calculate ELO rating and expected scores
def get_elo(i, df,elo, k):
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

    # Update ELO ratings
    elo[team_1] += k * (S_1 - ea_1)
    elo[team_2] += k * (S_2 - ea_2)

    return S_1, S_2, ea_1, ea_2

# Function to calculate MSE for a given K value over all seasons
def calculate_mse(k):
    total_mse = 0
    total_matches = 0

    # Loop through all dataframes (one for each season)
    for df in all_dataframes:
        # Reset ELO ratings at the start of each season
        elo = {team: 1500 for team in teams}

        # Calculate MSE for the current season
        season_mse = 0
        for i in range(len(df)):
            S_1, S_2, ea_1, ea_2 = get_elo(i, df, elo,k)

            # Calculate actual outcome: 1 if team 1 wins, else 0
            actual_outcome = 1 if S_1 > S_2 else 0

            # MSE calculation for team 1's expected score
            season_mse += (actual_outcome - ea_1) ** 2

        total_mse += season_mse
        total_matches += len(df)

    return total_mse / total_matches  # Average MSE over all matches

# List of file paths for the six seasons
file_paths = [
    r"C:/Users/rrpar/OneDrive/Desktop/UAAP WVB Eliminations/Season 79 Eliminations.csv",
    r"C:/Users/rrpar/OneDrive/Desktop/UAAP WVB Eliminations/Season 80 Eliminations.csv",
    r"C:/Users/rrpar/OneDrive/Desktop/UAAP WVB Eliminations/Season 81 Eliminations.csv",
    r"C:/Users/rrpar/OneDrive/Desktop/UAAP WVB Eliminations/Season 84 Eliminations.csv",
    r"C:/Users/rrpar/OneDrive/Desktop/UAAP WVB Eliminations/Season 85 Eliminations.csv",
    r"C:/Users/rrpar/OneDrive/Desktop/UAAP WVB Eliminations/Season 86 Eliminations.csv"
]

# Load all dataframes and clean them
all_dataframes = []
for file_path in file_paths:
    df = pd.read_csv(file_path, encoding='ISO-8859-1')
    df.dropna(how='all', axis=1, inplace=True)  # Remove empty columns
    all_dataframes.append(df)

# Extract all unique teams from all seasons
teams = pd.concat([df[['team1', 'team2']] for df in all_dataframes]).stack().unique()

# Finding the optimal K factor using MSE
k_values = range(100, 201, 1)  # Test K values (integers) from 10 to 50
mse_results = []

for k in k_values:
    mse = calculate_mse(k)
    mse_results.append((k, mse))
    print(f"K = {k}, MSE = {mse:.6f}")  # Print each K and its corresponding MSE

# Find the K value with the lowest MSE
optimal_k, lowest_mse = min(mse_results, key=lambda x: x[1])

# Print the optimal K value and the lowest MSE
print("\nOptimal K-factor:", optimal_k)
print("Lowest MSE:", lowest_mse)

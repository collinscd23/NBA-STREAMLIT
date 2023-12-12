import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Function to load the data
@st.cache
def load_data():
    data = pd.read_csv('NBA_player_data.csv')
    return data

# Function to plot a heatmap
def plot_heatmap(data, cols):
    plt.figure(figsize=(10, 8))
    sns.heatmap(data[cols].corr(), annot=True, cmap='coolwarm')
    plt.title('Statistical Correlation Heatmap')
    st.pyplot(plt)

# Function to plot a bar chart of top stats
def plot_top_stats(data, player_name):
    plt.figure(figsize=(10, 8))
    player_stats = data.iloc[0]
    stats = player_stats.drop(['Year', 'Season_type', 'PLAYER_ID', 'RANK', 'PLAYER', 'TEAM'])
    stats.sort_values(ascending=False, inplace=True)
    bar_chart = stats.head(10).plot(kind='bar')
    plt.title(f"Top 10 Stats for {player_name}")
    plt.ylabel('Stat Value')
    st.pyplot(plt)


# Function to compare two players
def compare_players(player1_data, player2_data, stats):
    player1_stats = player1_data[stats].mean()  # Using mean in case of multiple entries
    player2_stats = player2_data[stats].mean()

    for stat in stats:
        plt.figure(figsize=(8, 6))
        width = 0.35
        indices = [0, 1]  # Indices for two players

        plt.bar(indices[0], player1_stats[stat], width, label=player1_data['PLAYER'].iloc[0])
        plt.bar(indices[1], player2_stats[stat], width, label=player2_data['PLAYER'].iloc[0])

        plt.ylabel(stat)
        plt.title(f'Comparison of {stat}')
        plt.xticks(indices, [player1_data['PLAYER'].iloc[0], player2_data['PLAYER'].iloc[0]])
        plt.legend()

        st.pyplot(plt)

# Function to plot yearly trend for a given stat
def plot_yearly_trend(data, stat, season_type):
    yearly_data = data[data['Season_type'] == season_type].groupby('Year')[stat].mean()
    plt.figure(figsize=(10, 6))
    plt.plot(yearly_data, marker='o')
    plt.title(f'Yearly Trend in {stat} During {season_type}')
    plt.xlabel('Year')
    plt.ylabel(stat)
    st.pyplot(plt)

# Load the data
nba_data = load_data()

# Streamlit interface
st.title('NBA Player Stats Explorer')

# Single player analysis
st.header("Single Player Analysis")
player_name = st.text_input('Enter a player name').strip()

if player_name:
    player_data = nba_data[nba_data['PLAYER'].str.contains(player_name, case=False, na=False)]
    if not player_data.empty:
        st.write(player_data)

        heatmap_cols = ['GP', 'MIN', 'FGM', 'FGA', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'EFF']
        plot_heatmap(player_data, heatmap_cols)

        plot_top_stats(player_data, player_name)
    else:
        st.write('Player not found.')

# Player comparison
st.header("Player Comparison")
col1, col2 = st.columns(2)
with col1:
    player1_name = st.text_input("Enter first player's name", key="player1").strip()
with col2:
    player2_name = st.text_input("Enter second player's name", key="player2").strip()

comparison_stats = ['FG3M', 'FG3A', 'AST', 'PTS', 'STL', 'REB', 'FTM']
if player1_name and player2_name:
    player1_data = nba_data[nba_data['PLAYER'].str.contains(player1_name, case=False, na=False)]
    player2_data = nba_data[nba_data['PLAYER'].str.contains(player2_name, case=False, na=False)]

    if not player1_data.empty and not player2_data.empty:
        compare_players(player1_data, player2_data, comparison_stats)
    else:
        if player1_data.empty:
            st.write(f'Player {player1_name} not found.')
        if player2_data.empty:
            st.write(f'Player {player2_name} not found.')
            
# Yearly trend analysis for playoffs
st.header("Playoffs Yearly Trend Analysis")
selected_stat = st.selectbox('Select a stat to display trend', ['FG3M', 'POSS_est'], index=0)
plot_yearly_trend(nba_data, selected_stat, 'Playoffs')

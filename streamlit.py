import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Function to load the data
@st.cache
def load_data():
    data = pd.read_csv('NBA_player_data.csv')
    return data

# Function to plot a heatmap
def plot_heatmap(data, cols):
    corr_matrix = data[cols].corr()
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='coolwarm'))
    fig.update_layout(title='Statistical Correlation Heatmap', 
                      xaxis_nticks=36, yaxis_nticks=36)
    st.plotly_chart(fig)

# Function to plot a bar chart of top stats
def plot_top_stats(data, player_name):
    player_stats = data.iloc[0]
    stats = player_stats.drop(['Year', 'Season_type', 'PLAYER_ID', 'RANK', 'PLAYER', 'TEAM'])
    stats.sort_values(ascending=False, inplace=True)
    fig = px.bar(stats.head(10), title=f"Top 10 Stats for {player_name}")
    fig.update_layout(yaxis_title='Stat Value')
    st.plotly_chart(fig)


# Function to compare two players
def compare_players(player1_data, player2_data, stats):
    player1_stats = player1_data[stats].mean()
    player2_stats = player2_data[stats].mean()
    df = pd.DataFrame({'Stats': stats, player1_data['PLAYER'].iloc[0]: player1_stats, player2_data['PLAYER'].iloc[0]: player2_stats})
    fig = px.bar(df, x='Stats', y=[player1_data['PLAYER'].iloc[0], player2_data['PLAYER'].iloc[0]], barmode='group')
    fig.update_layout(title=f'Comparison of Players')
    st.plotly_chart(fig)

# Function to plot stat trends over the years
def plot_stat_trends(data, player_name, stats):
    player_data = data[data['PLAYER'] == player_name]
    player_data = player_data[player_data['Season_type'].str.contains('Playoffs')]

    # Ensure only years with data are included
    years_played = player_data['Year'].unique()

    for stat in stats:
        # Filter data to include only years played
        filtered_data = player_data[player_data['Year'].isin(years_played)]

        fig = px.line(filtered_data, x='Year', y=stat, title=f'{player_name} - {stat} Over Playoff Years')
        fig.update_layout(xaxis_title='Year', yaxis_title=stat)
        st.plotly_chart(fig)

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
            
# Stat trends over the years for playoffs
st.header("Player Stat Trends in Playoffs")
selected_player = st.selectbox("Select a Player", nba_data['PLAYER'].unique())

stats_to_plot = ['FG3M', 'FG3A', 'AST', 'PTS', 'STL', 'REB', 'FTM']
if selected_player:
    plot_stat_trends(nba_data, selected_player, stats_to_plot)



# Sample plot: Points per season
st.write("### Points per Season")
selected_season = st.selectbox('Select a Season', nba_data['Year'].unique())
filtered_data = nba_data[nba_data['Year'] == selected_season]
fig = px.bar(filtered_data, x='PLAYER', y='PTS', title=f'Points in Season {selected_season}')
st.plotly_chart(fig)

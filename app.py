import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 📂 Load data
@st.cache_data
def load_data():
    matches = pd.read_csv('data/matches.csv')
    deliveries = pd.read_csv('data/deliveries.csv')
    return matches, deliveries

matches, deliveries = load_data()

# 🎯 Filter Mumbai Indians matches
mi_matches = matches[(matches['team1'] == 'Mumbai Indians') | (matches['team2'] == 'Mumbai Indians')].copy()

# 🎨 Sidebar Navigation
st.sidebar.title("🏏 Mumbai Indians Analytics")
section = st.sidebar.radio("Choose Section", [
    "Overview",
    "Season-wise Wins",
    "Top Batsmen",
    "Top Bowlers",
    "Venue Performance",
    "Auction 2025 Strategy"
])

st.title("📊 Mumbai Indians - IPL Analytics Dashboard")

# 📌 Overview
if section == "Overview":
    st.subheader("🏆 Total Matches Played & Wins")
    total = len(mi_matches)
    wins = mi_matches[mi_matches['winner'] == 'Mumbai Indians'].shape[0]
    win_pct = round((wins / total) * 100, 2)
    st.metric("Total Matches", total)
    st.metric("Wins", wins)
    st.metric("Win %", win_pct)

    st.markdown("---")
    st.subheader("🎬 Season Participation")
    st.bar_chart(mi_matches['season'].value_counts().sort_index())

# 📈 Season-wise Wins
elif section == "Season-wise Wins":
    st.subheader("📅 Season-by-Season Wins")
    season_wins = mi_matches[mi_matches['winner'] == 'Mumbai Indians'].groupby('season').size()
    fig = px.bar(season_wins, x=season_wins.index, y=season_wins.values,
                 labels={'x': 'Season', 'y': 'Wins'}, color=season_wins.values,
                 title="Mumbai Indians Wins Per Season")
    st.plotly_chart(fig, use_container_width=True)

# 🔝 Top Batsmen
elif section == "Top Batsmen":
    st.subheader("🏏 Top Run Scorers for MI")
    mi_deliveries = deliveries[deliveries['batting_team'] == 'Mumbai Indians']
    top_batsmen = mi_deliveries.groupby('batter')['batsman_runs'].sum().sort_values(ascending=False).head(10)
    st.bar_chart(top_batsmen)

# 🎯 Top Bowlers
elif section == "Top Bowlers":
    st.subheader("🎯 Top Wicket Takers for MI")
    mi_dismissals = deliveries[(deliveries['bowling_team'] == 'Mumbai Indians') & (deliveries['dismissal_kind'].notna()) & (deliveries['dismissal_kind'] != 'run out')]
    top_bowlers = mi_dismissals.groupby('bowler').size().sort_values(ascending=False).head(10)
    st.bar_chart(top_bowlers)

# 🏟️ Venue Performance
elif section == "Venue Performance":
    st.subheader("📍 MI Venue-wise Match Wins")
    venue_wins = mi_matches[mi_matches['winner'] == 'Mumbai Indians'].groupby('venue').size().sort_values(ascending=False)
    fig = px.bar(venue_wins, x=venue_wins.values, y=venue_wins.index, orientation='h',
                 labels={'x': 'Wins', 'y': 'Venue'})
    st.plotly_chart(fig, use_container_width=True)

# 🛒 Auction Strategy
elif section == "Auction 2025 Strategy":
    st.subheader("🛒 Suggested Auction Strategy for 2025")
    st.markdown("""
    **Players to Retain:**  
    - Suryakumar Yadav  
    - Jasprit Bumrah  
    - Tilak Varma  

    **Consider Release / Trade:**  
    - Rohit Sharma (if transition planned)  
    - Piyush Chawla, Arjun Tendulkar, Nehal Wadhera  

    **Target Acquisitions:**  
    - **Powerplay Bowler:** Deepak Chahar, Mukesh Kumar  
    - **Finisher:** Riyan Parag, Abdul Samad  
    - **All-Rounder:** Washington Sundar  
    - **Backup Keeper:** Phil Salt, KS Bharat  
    """)

# ✅ Footer
st.markdown("---")
st.caption("👨‍💻 Created by Narendran | Streamlit App for MI IPL 2025 Strategy")

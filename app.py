import streamlit as st
import pandas as pd
import plotly.express as px
import random

# 📂 Load data
@st.cache_data
def load_data():
    matches = pd.read_csv('data/matches.csv')
    deliveries = pd.read_csv('data/deliveries.csv')
    return matches, deliveries

matches, deliveries = load_data()

# 🎯 Filter MI matches
mi_matches = matches[(matches['team1'] == 'Mumbai Indians') | (matches['team2'] == 'Mumbai Indians')].copy()

# 🎨 Sidebar Navigation
st.sidebar.title("🏏 Mumbai Indians Analytics")
section = st.sidebar.radio("Choose Section", [
    "Overview",
    "Season-wise Wins",
    "Top Batsmen",
    "Top Bowlers",
    "Venue Performance",
    "Auction 2025 Strategy",
    "Impact Player Suggestions",
    "Win Probability Calculator"
])
season_filter = st.sidebar.selectbox("Select Season (Optional)", ['All'] + sorted(mi_matches['season'].unique(), reverse=True))

# Optional filtering by season
if season_filter != 'All':
    mi_matches = mi_matches[mi_matches['season'] == season_filter]
    deliveries = deliveries[deliveries['match_id'].isin(mi_matches['id'])]

# 🧢 Main Title
st.title("📊 Mumbai Indians - IPL Analytics Dashboard")

# 📌 Overview
if section == "Overview":
    st.subheader("🏆 Total Matches Played & Wins")

    total = len(mi_matches)
    wins = mi_matches[mi_matches['winner'] == 'Mumbai Indians'].shape[0]
    win_pct = round((wins / total) * 100, 2)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Matches", total)
    col2.metric("Wins", wins)
    col3.metric("Win %", f"{win_pct}%")

    st.markdown("---")
    st.subheader("🎬 Season Participation")
    st.plotly_chart(
        px.bar(mi_matches['season'].value_counts().sort_index(),
               labels={'value': 'Matches', 'index': 'Season'},
               title="Season Participation"), use_container_width=True)

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
    mi_batting = deliveries[deliveries['batting_team'] == 'Mumbai Indians']
    top_batsmen = mi_batting.groupby('batter')['batsman_runs'].sum().sort_values(ascending=False).head(10).reset_index()
    fig = px.bar(top_batsmen, x='batter', y='batsman_runs',
                 labels={'batter': 'Batsman', 'batsman_runs': 'Runs'},
                 title="Top 10 Run Scorers")
    st.plotly_chart(fig, use_container_width=True)

# 🎯 Top Bowlers
elif section == "Top Bowlers":
    st.subheader("🎯 Top Wicket Takers for MI")
    mi_bowling = deliveries[(deliveries['bowling_team'] == 'Mumbai Indians') &
                            (deliveries['dismissal_kind'].notna()) &
                            (deliveries['dismissal_kind'] != 'run out')]
    top_bowlers = mi_bowling.groupby('bowler').size().sort_values(ascending=False).head(10).reset_index()
    top_bowlers.columns = ['bowler', 'wickets']
    fig = px.bar(top_bowlers, x='bowler', y='wickets',
                 labels={'bowler': 'Bowler', 'wickets': 'Wickets'},
                 title="Top 10 Wicket Takers")
    st.plotly_chart(fig, use_container_width=True)

# 🏟️ Venue Performance
elif section == "Venue Performance":
    st.subheader("📍 MI Venue-wise Match Wins")
    venue_wins = mi_matches[mi_matches['winner'] == 'Mumbai Indians'].groupby('venue').size().sort_values(ascending=False)
    venue_df = venue_wins.reset_index()
    venue_df.columns = ['venue', 'wins']
    fig = px.bar(venue_df, x='wins', y='venue', orientation='h',
                 title="Wins by Venue", labels={'wins': 'Wins', 'venue': 'Venue'})
    st.plotly_chart(fig, use_container_width=True)

# 🛒 Auction Strategy
elif section == "Auction 2025 Strategy":
    st.subheader("🛒 Suggested Auction Strategy for 2025")

    with st.expander("✅ Retain Core Players"):
        st.write("- Suryakumar Yadav: High strike rate and consistency")
        st.write("- Jasprit Bumrah: Death-over economy and match-winner")
        st.write("- Tilak Varma: Promising young talent")

    with st.expander("❌ Consider Release / Trade"):
        st.write("- Rohit Sharma: Ageing, possible leadership transition")
        st.write("- Piyush Chawla, Arjun Tendulkar, Nehal Wadhera")
        st.write("- Chris Jordan, Dewald Brevis, Riley Meredith (death economy)")

    with st.expander("📈 Target Acquisitions"):
        st.markdown("""
        - **Powerplay Bowler:** Deepak Chahar, Mukesh Kumar  
        - **Finisher:** Riyan Parag, Abdul Samad  
        - **All-Rounder:** Washington Sundar, Shahrukh Khan  
        - **Backup Wicketkeeper:** KS Bharat, Phil Salt  
        - **Death Backup:** Nandre Burger, Cottrell  
        """)

# 🔁 Impact Player Suggestions
elif section == "Impact Player Suggestions":
    st.subheader("🔁 Smart Usage of Impact Player for Mumbai Indians")
    st.markdown("### 💡 Match Scenarios & Ideal Substitutions")

    scenario = st.selectbox("Choose Match Scenario", [
        "Batting First – Need strong finish",
        "Bowling First – Need early wickets",
        "Chasing – Need middle overs acceleration",
        "Defending – Need death over control"
    ])

    if scenario == "Batting First – Need strong finish":
        st.write("👉 **Out:** Anchor-type top-order batter")
        st.write("👉 **In:** Finisher like *Abdul Samad* or *Riyan Parag*")

    elif scenario == "Bowling First – Need early wickets":
        st.write("👉 **Out:** Part-time bowler or batter")
        st.write("👉 **In:** *Mukesh Kumar* or *Mohsin Khan*")

    elif scenario == "Chasing – Need middle overs acceleration":
        st.write("👉 **Out:** Early dismissed opener")
        st.write("👉 **In:** *Tilak Varma* or *Shahrukh Khan*")

    elif scenario == "Defending – Need death over control":
        st.write("👉 **Out:** Spinner or expensive pacer")
        st.write("👉 **In:** *Jasprit Bumrah* or *Nandre Burger*")

    st.info("🧠 Use this rule tactically with toss, pitch, and game phase insights.")

# 🔮 Win Probability Calculator
elif section == "Win Probability Calculator":
    st.subheader("🔮 Quick Win Probability Estimator")

    st.markdown("📊 This is a simple utility based on score and overs.")
    current_score = st.number_input("Current Score", min_value=0, value=100)
    wickets = st.slider("Wickets Lost", 0, 10, 3)
    overs = st.slider("Overs Completed", 0.0, 20.0, 10.0, step=0.5)

    # Basic mock logic
    if overs == 0:
        win_chance = 0
    else:
        rr = current_score / overs
        win_chance = round(min(100, max(0, rr * (10 - wickets) + random.randint(-10, 10))), 2)

    st.metric("📈 Estimated Win %", f"{win_chance}%")

# ✅ Footer
st.markdown("---")
st.caption("👨‍💻 Created by Narendran | Streamlit App for MI IPL 2025 Strategy")

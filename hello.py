from preswald import connect, get_df, query, table, text, slider, plotly
import plotly.express as px
import pandas as pd

connect() 
df = get_df("sample_csv")  # Load ATP matches data

# converting the numeric columns to proper data types
df["winner_age"] = pd.to_numeric(df["winner_age"], errors='coerce')
df["loser_age"] = pd.to_numeric(df["loser_age"], errors='coerce')
df["minutes"] = pd.to_numeric(df["minutes"], errors='coerce')
df["w_ace"] = pd.to_numeric(df["w_ace"], errors='coerce')
df["w_svpt"] = pd.to_numeric(df["w_svpt"], errors='coerce')
df["w_1stIn"] = pd.to_numeric(df["w_1stIn"], errors='coerce')
df["w_bpFaced"] = pd.to_numeric(df["w_bpFaced"], errors='coerce')
df["w_bpSaved"] = pd.to_numeric(df["w_bpSaved"], errors='coerce')
df["winner_rank"] = pd.to_numeric(df["winner_rank"], errors='coerce')
df["loser_rank"] = pd.to_numeric(df["loser_rank"], errors='coerce')

# Query or manipulate the data
filtered_df = df[df["winner_age"] > 25]

text("# ATP Tennis Matches 2024 Analysis")

text("## 🏆 Tournament Champions & Key Stats")

# Tournament winners (finals only)
finals_df = df[df["round"] == "F"]
if not finals_df.empty:
    finals_summary = finals_df[["tourney_name", "winner_name", "loser_name", "score", "minutes"]].head(10)
    table(finals_summary, title="Tournament Finals - Champions")

# Most successful players
player_wins = df["winner_name"].value_counts().head(10).reset_index()
player_wins.columns = ["Player", "Tournament_Wins"]
table(player_wins, title="Most Tournament Wins in 2024")

text("## 🎾 Tennis Highlights")

# longest matches
longest_matches = df[df["minutes"].notna()].nlargest(5, "minutes")[["tourney_name", "winner_name", "loser_name", "score", "minutes"]]
table(longest_matches, title="Marathon Matches - Longest by Duration")

# most aces per match
ace_leaders = df[df["w_ace"].notna()].nlargest(5, "w_ace")[["tourney_name", "winner_name", "w_ace", "loser_name", "score"]]
table(ace_leaders, title="Ace Kings - Most Aces in a Single Match")

# biggest upsets 
upsets_df = df[(df["winner_rank"].notna()) & (df["loser_rank"].notna()) & 
               (df["winner_rank"] > df["loser_rank"] + 50)].copy()
if not upsets_df.empty:
    upsets_df["rank_difference"] = upsets_df["winner_rank"] - upsets_df["loser_rank"]
    biggest_upsets = upsets_df.nlargest(5, "rank_difference")[["tourney_name", "winner_name", "winner_rank", "loser_name", "loser_rank", "rank_difference", "score"]]
    table(biggest_upsets, title="Giant Killers - Biggest Ranking Upsets")

text("## 📊 Classic Tennis Analytics")

table(filtered_df.head(15), title="Matches with Winners Over 25 Years Old")

# Add user controls for age threshold
text("## Interactive Age Analysis")
age_threshold = slider("Age Threshold", min_val=18, max_val=40, default=25)
age_filtered_df = df[df["winner_age"] > age_threshold]
table(age_filtered_df[["tourney_name", "winner_name", "winner_age", "loser_name", "loser_age", "score"]].head(15), 
      title="Dynamic Data View - Winners Above Age Threshold")

# tournie visualization
text("## 🏟️ Tournament Analysis")
tournament_counts = df.groupby("tourney_name").size().reset_index(name="match_count")
tournament_counts = tournament_counts.sort_values("match_count", ascending=False).head(15)

fig_tournaments = px.bar(
    tournament_counts,
    x="tourney_name",
    y="match_count",
    title="Tournament Size by Number of Matches",
    labels={"tourney_name": "Tournament", "match_count": "Number of Matches"},
    color="match_count",
    color_continuous_scale="viridis"
)
fig_tournaments.update_layout(xaxis_tickangle=45)
plotly(fig_tournaments)

# rivalries
text("## ⚔️ Player Rivalries")
# head-to-head matchups
h2h_data = []
for _, match in df.iterrows():
    winner = match['winner_name']
    loser = match['loser_name']
    if pd.notna(winner) and pd.notna(loser):
        players = sorted([winner, loser])
        matchup = f"{players[0]} vs {players[1]}"
        winner_in_matchup = winner
        h2h_data.append({'matchup': matchup, 'winner': winner_in_matchup, 'tournament': match['tourney_name']})

h2h_df = pd.DataFrame(h2h_data)
if not h2h_df.empty:
    # counting most frequent matchups
    frequent_matchups = h2h_df['matchup'].value_counts().head(10)
    if len(frequent_matchups) > 1:  # Only show if there are actual rivalries
        fig_rivalries = px.bar(
            x=frequent_matchups.values,
            y=frequent_matchups.index,
            orientation='h',
            title="Most Frequent Player Matchups in 2024",
            labels={"x": "Number of Matches", "y": "Player Matchup"}
        )
        plotly(fig_rivalries)

# age analysis
text("## Age Distribution Analysis")
fig_age = px.histogram(
    df,
    x="winner_age",
    nbins=20,
    title="Distribution of Winner Ages",
    labels={"winner_age": "Winner Age", "count": "Frequency"}
)
plotly(fig_age)

# match time analysis
text("## Match Duration Analysis")
duration_df = df[df["minutes"].notna() & (df["minutes"] > 0)]
fig_duration = px.scatter(
    duration_df,
    x="winner_age",
    y="minutes",
    color="surface",
    title="Match Duration vs Winner Age by Surface",
    labels={"winner_age": "Winner Age", "minutes": "Match Duration (minutes)", "surface": "Court Surface"}
)
plotly(fig_duration)

# grass v clay v hard surface analysis
text("## Surface Performance Analysis")
surface_stats = df.groupby("surface").agg({
    "minutes": "mean",
    "tourney_name": "count"
}).reset_index()
surface_stats.columns = ["surface", "avg_duration", "match_count"]

fig_surface = px.bar(
    surface_stats,
    x="surface",
    y="avg_duration",
    title="Average Match Duration by Court Surface",
    labels={"surface": "Court Surface", "avg_duration": "Average Duration (minutes)"}
)
plotly(fig_surface)

# country/nationality analysis
text("## Player Nationality Distribution")
nationality_counts = df["winner_ioc"].value_counts().head(15).reset_index()
nationality_counts.columns = ["country", "wins"]

fig_nationality = px.pie(
    nationality_counts,
    values="wins",
    names="country",
    title="Top 15 Countries by Tournament Wins"
)
plotly(fig_nationality)

# serve analysis
text("## 🎯 Serve Performance Analysis")
serve_df = df[df["w_ace"].notna() & df["w_svpt"].notna() & (df["w_svpt"] > 0) & df["minutes"].notna() & (df["minutes"] > 0)]
serve_df["ace_percentage"] = (serve_df["w_ace"] / serve_df["w_svpt"]) * 100

# First serve percentage analysis
serve_df["first_serve_pct"] = (serve_df["w_1stIn"] / serve_df["w_svpt"]) * 100

fig_serve = px.scatter(
    serve_df,
    x="first_serve_pct",
    y="ace_percentage",
    color="surface",
    size="minutes",
    hover_data=["winner_name", "tourney_name"],
    title="First Serve % vs Ace % - Serving Effectiveness by Surface",
    labels={
        "first_serve_pct": "First Serve Percentage (%)",
        "ace_percentage": "Ace Percentage (%)",
        "surface": "Court Surface",
        "minutes": "Match Duration"
    }
)
plotly(fig_serve)

# break point conversion analysis
text("## 🏹 Clutch Performance - Break Points")
bp_df = df[(df["w_bpFaced"].notna()) & (df["w_bpSaved"].notna()) & (df["w_bpFaced"] > 0)]
bp_df["bp_save_pct"] = (bp_df["w_bpSaved"] / bp_df["w_bpFaced"]) * 100

fig_bp = px.histogram(
    bp_df,
    x="bp_save_pct",
    nbins=20,
    title="Break Point Save Percentage Distribution",
    labels={"bp_save_pct": "Break Point Save Percentage (%)", "count": "Number of Matches"}
)
plotly(fig_bp)

text("## Summary")
total_matches = len(df)
total_tournaments = df['tourney_name'].nunique()
avg_age = df['winner_age'].mean()
most_common_surface = df['surface'].mode()

summary_text = f"Dataset contains {total_matches} matches from {total_tournaments} tournaments. "
if pd.notna(avg_age):
    summary_text += f"Average winner age: {avg_age:.1f} years. "
if len(most_common_surface) > 0:
    summary_text += f"Most common surface: {most_common_surface.iloc[0]}."

text(summary_text)
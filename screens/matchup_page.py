import streamlit as st
import pandas as pd
from utils.loaders import load_match_data, load_reference_data
from utils.enrich import enrich_data
from utils.filters import apply_matchup_filters
from DataDir import matchup_stats_dir

@st.cache_data
def load_matchup_stats():
    return pd.read_csv(matchup_stats_dir)

def show_matchup_page():
    refs = load_reference_data()
    raw_df = enrich_data(load_matchup_stats(), refs)
    match_df = enrich_data(load_match_data(), refs)

    # Add team1 vs team2 for context
    match_ids = raw_df["match_id"].unique().tolist()
    match_lookup = match_df[match_df["match_id"].isin(match_ids)][["match_id", "team1", "team2"]].copy()
    match_lookup.columns = ["match_id", "match_team1", "match_team2"]
    raw_df = raw_df.merge(match_lookup, how="left", on="match_id")
    raw_df["match"] = raw_df["match_team1"] + " vs " + raw_df["match_team2"]
    raw_df.drop(columns=["match_team1", "match_team2"], inplace=True)

    # Sort by date descending
    raw_df["date"] = pd.to_datetime(raw_df["date"], errors='coerce')
    raw_df = raw_df.dropna(subset=["date"])
    raw_df = raw_df.sort_values("date", ascending=False).reset_index(drop=True)

    # Apply filters
    filtered_df, selected_bowler, match_limit = apply_matchup_filters(raw_df.copy())

    if filtered_df is None:
        st.warning("Please select a Batter to view matchup statistics.")
        return

    match_count = filtered_df["match_id"].nunique()
    if match_limit > 0:
        st.info(f"Matches found: {match_count}. Showing last {match_limit} matches.")
    else:
        st.info(f"Matches found: {match_count}. Showing full history.")

    if match_limit > 0:
        filtered_df = filtered_df.sort_values("date", ascending=False).groupby("match_id").head(1)
        filtered_df = filtered_df.head(match_limit)

    if not filtered_df.empty:
        total_runs = filtered_df["total_runs"].sum()
        balls_faced = filtered_df["balls_faced"].sum()
        fours = filtered_df["fours"].sum()
        sixes = filtered_df["sixes"].sum()
        boundaries = filtered_df["total_boundaries"].sum()
        strike_rate = round((total_runs / balls_faced) * 100, 2) if balls_faced > 0 else 0

        dismissals = filtered_df[filtered_df["wicket_flag"] == 1]
        total_dismissals = len(dismissals)
        dismissal_types = dismissals["wicket_type"].value_counts().to_dict()

        selected_batter = st.session_state.get("matchup_batter")

        summary = {
            "Batter": selected_batter,
            "Bowler": selected_bowler if selected_bowler != "None" else "All",
            "Total Runs": total_runs,
            "Balls Faced": balls_faced,
            "4s": fours,
            "6s": sixes,
            "Total Boundaries": boundaries,
            "Strike Rate": strike_rate,
            "Total Dismissals": total_dismissals,
            "Dismissal Types": ", ".join([f"{k} ({v})" for k, v in dismissal_types.items()]) if dismissal_types else "None"
        }

        st.markdown("### Matchup Summary")
        st.dataframe(pd.DataFrame([summary]).reset_index(drop=True))

        st.markdown("### Matchup Data")
        display_df = filtered_df.drop(columns=["match_id"]).reset_index(drop=True)
        st.dataframe(display_df)
    else:
        st.info("No matchup data available for the selected filters.")

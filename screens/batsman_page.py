import streamlit as st
import pandas as pd
from utils.loaders import load_batsman_stats, load_match_data, load_reference_data
from utils.enrich import enrich_data
from utils.filters import apply_batsman_filters


def show_batsman_page():
    refs = load_reference_data()
    raw_df = enrich_data(load_batsman_stats(), refs)
    match_df = enrich_data(load_match_data(), refs)

    # Add team1 vs team2 to raw data
    match_ids = raw_df["match_id"].unique().tolist()
    match_lookup = match_df[match_df["match_id"].isin(match_ids)][["match_id", "team1", "team2"]].copy()
    match_lookup.columns = ["match_id", "match_team1", "match_team2"]
    raw_df = raw_df.merge(match_lookup, how="left", on="match_id")
    raw_df["match"] = raw_df["match_team1"] + " vs " + raw_df["match_team2"]
    raw_df.drop(columns=["match_team1", "match_team2"], inplace=True)

    # Sort by date descending
    raw_df["date"] = pd.to_datetime(raw_df["date"], errors='coerce')
    raw_df = raw_df.sort_values("date", ascending=False).reset_index(drop=True)

    # Sidebar input for match count
    with st.sidebar:
        st.markdown("### Stats Settings")
        match_limit = st.number_input("Show stats for last X matches", min_value=1, max_value=100, value=5)

    # Apply filters
    filtered_df = apply_batsman_filters(raw_df.copy())

    st.subheader("Batsman Statistics")

    # Stats Section
    selected_batter = st.session_state.get("bat_batter")  # comes from selectbox key in filters
    if selected_batter and selected_batter != "All":
        batter_df = filtered_df[filtered_df["batter"] == selected_batter].head(match_limit)

        # Build dynamic heading from all sidebar filters
        filters = {
            "event_name": "Event",
            "match_type": "Match Type",
            "team_type": "Team Type",
            "city": "City",
            "venue": "Venue"
        }

        heading_parts = [f"Stats For Last {match_limit} Matches for {selected_batter}"]
        for key, label in filters.items():
            val = st.session_state.get(f"bat_{key}")
            if val and val != "All":
                heading_parts.append(f"{label}: {val}")
        heading = ", ".join(heading_parts)

        if not batter_df.empty:
            if len(batter_df) < match_limit:
                st.warning(f"Only {len(batter_df)} match(es) available for the selected filters. Showing available data.")

            summary = {
                "Batsman": selected_batter,
                "Average Runs": round(batter_df["total_runs"].mean(), 2),
                "Average Balls Faced": round(batter_df["balls_faced"].mean(), 2),
                "Average 4s": round(batter_df["fours"].mean(), 2),
                "Average 6s": round(batter_df["sixes"].mean(), 2),
                "Average Boundaries": round(batter_df["total_boundaries"].mean(), 2),
                "Average Strike Rate": round(batter_df["strike_rate"].mean(), 2),
                "Average Runs Per Over": round(batter_df["avg_runs_per_over"].mean(), 2),
            }

            st.markdown(f"### {heading}")
            st.dataframe(pd.DataFrame([summary]).reset_index(drop=True))

            st.markdown("### Data Used for Stats")
            batter_df_display = batter_df.drop(columns=["match_id"]) if "match_id" in batter_df.columns else batter_df
            st.dataframe(batter_df_display.reset_index(drop=True))

        else:
            st.info("No data found for the selected batsman and filters.")
    else:
        st.warning("Please select a Batsman in the filters to view statistics.")

    # Raw data section
    st.markdown("### Batsman Data")
    final_display = filtered_df.drop(columns=["match_id"]) if "match_id" in filtered_df.columns else filtered_df
    st.dataframe(final_display.reset_index(drop=True))

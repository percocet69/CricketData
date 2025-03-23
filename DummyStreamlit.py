import streamlit as st
import pandas as pd
from DataDir import indicator_city_dir, indicator_venue_dir, indicator_event_name_dir, indicator_event_stage_dir, \
    indicator_match_type_dir, indicator_team_type_dir, indicator_teams_dir, indicator_players_dir, match_innings_dir, match_data_dir


# Load main data
@st.cache_data
def load_match_innings_data():
    return pd.read_csv(match_innings_dir)

@st.cache_data
def load_match_data():
    return pd.read_csv(match_data_dir)

# Load reference data
@st.cache_data
def load_reference_data():
    refs = {
        "city": pd.read_csv(indicator_city_dir),
        "venue": pd.read_csv(indicator_venue_dir),
        "event_name": pd.read_csv(indicator_event_name_dir),
        "event_stage": pd.read_csv(indicator_event_stage_dir),
        "match_type": pd.read_csv(indicator_match_type_dir),
        "team_type": pd.read_csv(indicator_team_type_dir),
        "teams": pd.read_csv(indicator_teams_dir),
        "players": pd.read_csv(indicator_players_dir),
    }
    return refs

# Merge all reference fields into main data
def enrich_data(df, refs):
    df = df.copy()

    ref_mappings = {
        "city": ("city_id", "city"),
        "venue": ("venue_id", "venue"),
        "event_name": ("event_name_id", "event_name"),
        "event_stage": ("event_stage_id", "event_stage"),
        "match_type": ("match_type_id", "match_type"),
        "team_type": ("team_type_id", "team_type"),
        "teams": ("team_id", "team_name"),
        "players": ("player_id", "player")
    }

    field_to_ref = {
        "city": "city",
        "venue": "venue",
        "event_name": "event_name",
        "event_stage": "event_stage",
        "match_type": "match_type",
        "team_type": "team_type",
        "team1": "teams",
        "team2": "teams",
        "toss_winner": "teams",
        "outcome_winner": "teams",
        "player_of_match": "players"
    }

    for field, ref_key in field_to_ref.items():
        id_col, name_col = ref_mappings[ref_key]
        ref_df = refs[ref_key][[id_col, name_col]].copy()
        mapping_dict = ref_df.set_index(id_col)[name_col].to_dict()
        if field in df.columns:
            df[field] = df[field].map(mapping_dict)

    return df

# Apply filters based on multiple fields
def apply_filters(df):
    with st.sidebar:
        st.markdown("### Filters")

        all_teams = sorted(set(df["team1"].dropna().unique()) | set(df["team2"].dropna().unique()))
        playing_team = st.selectbox("Playing Team", options=["None"] + all_teams)

        if playing_team != "None":
            df = df[(df["team1"] == playing_team) | (df["team2"] == playing_team)]
            opponents = sorted(set(df.loc[df["team1"] == playing_team, "team2"].dropna().unique())
                               | set(df.loc[df["team2"] == playing_team, "team1"].dropna().unique()))
            opponent_team = st.selectbox("Opponent Team", options=["None"] + opponents)

            if opponent_team != "None":
                df = df[((df["team1"] == playing_team) & (df["team2"] == opponent_team)) |
                        ((df["team1"] == opponent_team) & (df["team2"] == playing_team))]

        filter_fields = [
            "venue", "event_name", "match_type", "team_type", "city", "won_by"
        ]

        for field in filter_fields:
            if field in df.columns:
                options = ["All"] + sorted(df[field].dropna().unique().tolist())
                selection = st.selectbox(f"Filter by {field.replace('_', ' ').title()}", options, key=field)
                if selection != "All":
                    df = df[df[field] == selection]

        if "date" in df.columns and not df.empty:
            df["date"] = pd.to_datetime(df["date"], errors='coerce')
            df = df.dropna(subset=["date"])
            if not df.empty:
                min_date = df["date"].min().date()
                max_date = df["date"].max().date()
                date_range = st.date_input("Filter by Date Range", [min_date, max_date])
                if len(date_range) == 2:
                    df = df[(df["date"].dt.date >= date_range[0]) & (df["date"].dt.date <= date_range[1])]

    return df

# Streamlit UI
def main():
    st.title("Cricket Match Data Viewer")

    if "view_section" not in st.session_state:
        st.session_state.view_section = "innings"

    with st.sidebar:
        st.markdown("### Select Dataset")
        if st.button("Match Summary Data"):
            st.session_state.view_section = "summary"
        if st.button("Match Innings Data"):
            st.session_state.view_section = "innings"

    refs = load_reference_data()

    if st.session_state.view_section == "innings":
        df = load_match_innings_data()
        enriched_df = enrich_data(df, refs)
        enriched_df = apply_filters(enriched_df)
        st.subheader("Match Innings Data")
        st.dataframe(enriched_df)

    elif st.session_state.view_section == "summary":
        df = load_match_data()
        enriched_df = enrich_data(df, refs)
        enriched_df = apply_filters(enriched_df)
        st.subheader("Match Summary Data")
        st.dataframe(enriched_df)

if __name__ == "__main__":
    main()
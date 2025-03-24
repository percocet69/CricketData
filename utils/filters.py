import streamlit as st
import pandas as pd


def apply_filters(df):
    with st.sidebar:
        st.markdown("### Filters")
        if "team1" in df.columns and "team2" in df.columns:
            all_teams = sorted(set(df["team1"].dropna()) | set(df["team2"].dropna()))
            playing_team = st.selectbox("Playing Team", options=["None"] + all_teams)
            if playing_team != "None":
                df = df[(df["team1"] == playing_team) | (df["team2"] == playing_team)]
                opponents = sorted(set(df.loc[df["team1"] == playing_team, "team2"].dropna())
                                   | set(df.loc[df["team2"] == playing_team, "team1"].dropna()))
                opponent_team = st.selectbox("Opponent Team", options=["None"] + opponents)
                if opponent_team != "None":
                    df = df[((df["team1"] == playing_team) & (df["team2"] == opponent_team)) |
                            ((df["team1"] == opponent_team) & (df["team2"] == playing_team))]

        for field in ["venue", "event_name", "match_type", "team_type", "city", "won_by"]:
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


def apply_batsman_filters(df):
    with st.sidebar:
        st.markdown("### Batsman Filters")

        # Batsman filter
        if "batter" in df.columns:
            batters = sorted(df["batter"].dropna().unique())
            selected_batter = st.selectbox("Batsman", ["All"] + batters, key="bat_batter")
            if selected_batter != "All":
                df = df[df["batter"] == selected_batter]

        # Categorical filters (venue, event_name, etc.)
        cat_filters = ["city", "venue", "event_name", "match_type", "team_type"]
        for field in cat_filters:
            if field in df.columns:
                options = ["All"] + sorted(df[field].dropna().unique())
                selection = st.selectbox(f"{field.replace('_', ' ').title()}", options, key=f"bat_{field}")
                if selection != "All":
                    df = df[df[field] == selection]

        # Date range
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], errors='coerce')
            df = df.dropna(subset=["date"])
            if not df.empty:
                min_date = df["date"].min().date()
                max_date = df["date"].max().date()
                date_range = st.date_input("Date Range", [min_date, max_date])
                if len(date_range) == 2:
                    df = df[(df["date"].dt.date >= date_range[0]) & (df["date"].dt.date <= date_range[1])]

        # Numeric filters
        numeric_fields = ["total_runs", "balls_faced", "fours", "sixes", "strike_rate", "avg_runs_per_over"]
        for field in numeric_fields:
            if field in df.columns:
                min_val = float(df[field].min())
                max_val = float(df[field].max())

                if min_val < max_val:
                    selected_range = st.slider(
                        f"{field.replace('_', ' ').title()} Range",
                        min_val, max_val, (min_val, max_val)
                    )
                    df = df[(df[field] >= selected_range[0]) & (df[field] <= selected_range[1])]
                else:
                    st.info(f"Not enough variation in **{field.replace('_', ' ').title()}** to apply a filter.")

    return df

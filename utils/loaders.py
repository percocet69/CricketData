import pandas as pd
from DataDir import (
    match_innings_dir, match_data_dir, batsman_stats_dir,
    indicator_city_dir, indicator_venue_dir, indicator_event_name_dir, indicator_event_stage_dir,
    indicator_match_type_dir, indicator_team_type_dir, indicator_teams_dir, indicator_players_dir
)

def load_match_innings_data():
    return pd.read_csv(match_innings_dir)

def load_match_data():
    return pd.read_csv(match_data_dir)

def load_batsman_stats():
    return pd.read_csv(batsman_stats_dir)

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
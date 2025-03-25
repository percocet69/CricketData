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
        "players": ("player_id", "player"),
        "wicket_type": ("wicket_type_id", "wicket_type")
    }
    field_to_ref = {
        "city": "city", "venue": "venue", "event_name": "event_name", "event_stage": "event_stage",
        "match_type": "match_type", "team_type": "team_type", "team1": "teams", "team2": "teams",
        "toss_winner": "teams", "outcome_winner": "teams", "player_of_match": "players", "batter": "players",
        "wicket_type": "wicket_type"
    }
    for field, ref_key in field_to_ref.items():
        id_col, name_col = ref_mappings[ref_key]
        ref_df = refs[ref_key][[id_col, name_col]].copy()
        mapping_dict = ref_df.set_index(id_col)[name_col].to_dict()
        if field in df.columns:
            df[field] = df[field].map(mapping_dict)
    return df

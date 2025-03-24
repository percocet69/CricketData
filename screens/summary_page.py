import streamlit as st
from utils.loaders import load_match_data, load_reference_data
from utils.enrich import enrich_data
from utils.filters import apply_filters

def show_summary_page():
    refs = load_reference_data()
    df = load_match_data()
    df = enrich_data(df, refs)
    df = apply_filters(df)
    st.subheader("Match Summary Data")
    st.dataframe(df)
import streamlit as st
from screens.innings_page import show_innings_page
from screens.summary_page import show_summary_page
from screens.batsman_page import show_batsman_page
from screens.matchup_page import show_matchup_page
from screens.readme_page import show_readme_page


st.set_page_config(page_title="Cricket Match Viewer", layout="wide")
st.title("Cricket Match Data Viewer")

if "view_section" not in st.session_state:
    st.session_state.view_section = "readme"

with st.sidebar:
    st.markdown("### Select Dataset")
    if st.button("ReadMe / Project Info"):
        st.session_state.view_section = "readme"
    if st.button("Match Summary Data"):
        st.session_state.view_section = "summary"
    # if st.button("Match Innings Data"):
    #     st.session_state.view_section = "innings"
    if st.button("Batsman Statistics"):
        st.session_state.view_section = "batsman"
    if st.button("Matchup Statistics"):
        st.session_state.view_section = "matchup"

if st.session_state.view_section == "summary":
    show_innings_page()
# elif st.session_state.view_section == "innings":
#     show_summary_page()
elif st.session_state.view_section == "batsman":
    show_batsman_page()
elif st.session_state.view_section == "matchup":
    show_matchup_page()
elif st.session_state.view_section == "readme":
    show_readme_page()

st.markdown(
    """
    <hr style="margin-top: 3em; margin-bottom: 1em">
    <div style="font-size: 0.9em; color: gray; text-align: center;">
        Data sourced from <a href="https://cricsheet.org" target="_blank">Cricsheet</a>, available under the 
        <a href="https://opendatacommons.org/licenses/by/1-0/" target="_blank">Open Data Commons Attribution License (ODC-By v1.0)</a>.<br>
        This is a personal learning project. Data may be incomplete or inaccurate. Use at your own discretion.
    </div>
    """,
    unsafe_allow_html=True
)

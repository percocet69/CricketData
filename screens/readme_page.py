import streamlit as st

def show_readme_page():
    st.title("📘 Project Overview & ReadMe")

    st.markdown("""
    ### 🎯 Project Purpose
    This is a personal project built to explore and analyze detailed cricket match data in a structured, interactive way.

    The motivation behind this project was to:
    - Learn and improve data wrangling and visualization skills
    - Gain experience with Streamlit and modular Python apps
    - Explore cricket stats from a fan’s perspective using ball-level detail

    ---

    ### 📊 Data Source & License
    - All match data has been sourced from **[Cricsheet](https://cricsheet.org)**.
    - The original data is provided in raw JSON format and is made available under the [Open Data Commons Attribution License (ODC-By) v1.0](https://opendatacommons.org/licenses/by/1-0/).
    - This project modifies and processes that raw data to derive structured tables and analytical insights.

    ---

    ### 🛠️ How the Data is Used
    - The JSON data has been cleaned, normalized, and enriched using reference tables.
    - Derived statistics include batter stats, batter vs bowler matchups, innings summaries, and more.

    The data shown here spans from **19th December 2001 to 6th March 2025** (note: matches from the current IPL season are **not** yet included).

    ---

    ### 👨‍🎓 About Me
    I recently completed my MBA and am currently waiting to start my full-time job. During this transition period, I'm taking time to:
    - Learn new tools and frameworks
    - Sharpen my coding and data analysis skills
    - Apply my interests (like cricket) to hands-on learning

    This app represents both my passion for the game and my commitment to continuous learning.

    ---

    ### ⚠️ Accuracy Disclaimer
    I’ve done my best to ensure data accuracy while transforming it from raw JSON to the current format. However:
    - Errors may exist in transformation logic or calculations
    - This is a **learning project**, and I welcome constructive feedback

    ---

    ### 🔮 What’s Next?
    I plan to:
    - Add charts/graphs for visual insights 📈
    - Expand filtering and comparison tools

    Adding newer match data is very tedious at the moment. And it may not be done.
    There is no timeline commitment for any changes. I will do it as and when I get time.

    ---

    ### 🙌 Open Use
    If you'd like to use or build upon the data presented here:
    - You are absolutely free to do so!
    - A simple credit to this project would be appreciated 🙏

    Anyone is free to use the site and the insights shared here for personal or educational purposes. However, please note that this project was built purely for learning, and I do not make any guarantees regarding the accuracy or completeness of the data, calculations, or inferences shown.

    By using the site, you acknowledge that the data may be incomplete or contain errors, and you agree that I will not be held liable for any use, interpretation, or decisions made based on this content.
    
    Thanks for checking it out!
    """)

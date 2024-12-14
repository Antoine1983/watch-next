import streamlit as st

pg = st.navigation(
    [
        st.Page("page_roulette.py", title="Find a movie", icon="🎥"),
        st.Page("page_statistics.py", title="About")
    ]
)

pg.run()

import streamlit as st

pg = st.navigation(
    [
        st.Page("page_top_movies.py", title="Top movies", icon="🏅"),
        st.Page("page_roulette.py", title="Movie Roulette", icon="🔀"),
        st.Page("page_statistics.py", title="Stats", icon="📈")
    ]
)

pg.run()

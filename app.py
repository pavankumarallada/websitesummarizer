import streamlit as st
from summarizer import summarize

st.set_page_config(
    page_title="AI Website Summarizer",
    layout="wide"
)

# Session State
if "summary" not in st.session_state:
    st.session_state.summary = ""

# Title
st.markdown(
    "<h1 style='text-align:center;'>🔎 AI Website Summarizer</h1>",
    unsafe_allow_html=True
)

# Two-column layout
col1, col2 = st.columns([1, 1])

# Left Panel
with col1:

    st.subheader("Website URL")

    url = st.text_input(
        "",
        placeholder="https://www.python.org"
    )

    c1, c2 = st.columns(2)

    with c1:
        clear = st.button("Clear")

    with c2:
        submit = st.button("Submit")

    if clear:
        st.session_state.summary = ""
        st.rerun()

    if submit:

        if not url:
            st.warning("Please enter a URL")
        else:

            with st.spinner("Summarizing website..."):

                try:
                    st.session_state.summary = summarize(url)

                except Exception as e:
                    st.error(f"Error: {e}")

# Right Panel
with col2:

    if st.session_state.summary:

        st.markdown("## Quick Glimpse")

        st.markdown(st.session_state.summary)

        st.button("🚩 Flag")
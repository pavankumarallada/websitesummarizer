
import streamlit as st
from summarizer import summarize

st.set_page_config(
    page_title="AI Website Summarizer",
    layout="wide"
)

# Initialize session state
if "summary" not in st.session_state:
    st.session_state.summary = ""

if "url" not in st.session_state:
    st.session_state.url = ""

# Application title
st.markdown(
    "<h1 style='text-align:center;'>🔎 AI Website Summarizer</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center;'>Enter a website URL to generate "
    "a concise AI-powered summary.</p>",
    unsafe_allow_html=True
)

# Two-column layout
col1, col2 = st.columns([1, 1], gap="large")

# Left panel
with col1:
    st.subheader("Website URL")

    url = st.text_input(
        "Website address",
        key="url",
        placeholder="https://www.python.org",
        label_visibility="collapsed"
    )

    c1, c2 = st.columns(2)

    with c1:
        clear = st.button("Clear", use_container_width=True)

    with c2:
        submit = st.button(
            "Submit",
            type="primary",
            use_container_width=True
        )

    if clear:
        st.session_state.summary = ""
        st.session_state.url = ""
        st.rerun()

    if submit:
        if not url.strip():
            st.warning("Please enter a website URL.")

        else:
            # Clear the previous summary before a new request
            st.session_state.summary = ""

            try:
                with st.spinner("Fetching and summarizing website..."):
                    result = summarize(url.strip())

                st.session_state.summary = result
                st.success("Website summarized successfully.")

            except (ValueError, RuntimeError) as e:
                st.error(str(e))

            except Exception as e:
                st.error(
                    "An unexpected error occurred while processing "
                    f"the website: {e}"
                )

# Right panel
with col2:
    st.subheader("Quick Glimpse")

    if st.session_state.summary:
        st.markdown(st.session_state.summary)

        st.divider()

        if st.button("🚩 Flag"):
            st.info("Flag button clicked.")
    else:
        st.info(
            "Your website summary will appear here after you submit a URL."
        )

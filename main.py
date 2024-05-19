import streamlit as st
from essay_scoring_tab import render_essay_scoring_tab


# Replicate Credentials
with st.sidebar:
    st.title('Learn Mentor')
    if 'REPLICATE_API_TOKEN' in st.secrets:
        replicate_api_token = st.secrets['REPLICATE_API_TOKEN']
    else:
        replicate_api_token = st.text_input('Enter Replicate API token:', type='password')
        if not (replicate_api_token.startswith('r8_') and len(replicate_api_token)==40):
            st.markdown("**Don't have an API token?** Head over to [Replicate](https://replicate.com) to sign up for one.")


    st.session_state['REPLICATE_API_TOKEN'] = replicate_api_token

st.header("Learn Mentor", divider="rainbow")
st.markdown("Accessible Assistants Using Snowflake's **Arctic** LLM")

grading_tab, = st.tabs(["Essay Mentor"])

with grading_tab:
    render_essay_scoring_tab()
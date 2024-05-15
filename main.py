import streamlit as st
from grading_tab import render_grading_tab


st.header("Educational Assistants", divider="rainbow")
st.subheader("Accessible Assistants Using Snowflake's Arctic LLM")

grading_tab, = st.tabs(["Essay Mentor"])

with grading_tab:
    render_grading_tab()
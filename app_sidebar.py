import streamlit as st
from typing import Callable, Optional
from utils import is_valid_token

def initialise_replicate_auth_token():
    if 'REPLICATE_API_TOKEN' in st.session_state and is_valid_token(st.session_state['REPLICATE_API_TOKEN']):
        return
    
    if 'REPLICATE_API_TOKEN' in st.secrets:
        replicate_api_token = st.secrets['REPLICATE_API_TOKEN']
    else:
        st.subheader('Learn Mentor Settings')
        replicate_api_token = st.text_input('Enter Replicate API token:', type='password')
        if not is_valid_token(replicate_api_token):
            st.caption("**Don't have an API token?** Head over to [Replicate](https://replicate.com) to sign up for one.")


    st.session_state['REPLICATE_API_TOKEN'] = replicate_api_token


def app_sidebar(renderExtras: Optional[Callable[[], None]] = None):
    with st.sidebar:
        initialise_replicate_auth_token()

        if renderExtras is not None:
            renderExtras()
import streamlit as st

icons = {"assistant": "👩", "user": "👨‍🎓"}

def initialise_session(name: str):
    if name not in st.session_state.keys():
        st.session_state[name] = {"messages": []}

def display_messages(session_state: str): 
    for message in st.session_state[session_state]["messages"]:
        with st.chat_message(message["role"], avatar=icons[message["role"]]):
            st.write(message["content"])

def clear_chat_history(session_name: str):
    st.session_state[session_name] = {"messages": []}

def write_message(message):
    with st.chat_message(message["role"], avatar=icons[message["role"]]):
        st.write(message["content"])   
        

def write_message_and_add_to_history(message: str, role: str, session_name: str):
    message = {"role": role, "content": message}
    with st.chat_message(message["role"], avatar=icons[message["role"]]):
        st.write(message["content"])   
    st.session_state[session_name]["messages"].append(message)

def show_all_session_chat_messages(session_name: str):  
    if session_name in st.session_state.keys():
        for message in st.session_state[session_name]["messages"]:
            write_message(message)
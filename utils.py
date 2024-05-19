
import streamlit as st
from transformers import AutoTokenizer
import replicate

# Set assistant icon to Snowflake logo
icons = {"assistant": "👁", "user": "⛷️"}
def display_messages(): 
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=icons[message["role"]]):
            st.write(message["content"])

def clear_chat_history(greeting: str | None = None):
    greeting = greeting or "Hi. I'm Arctic, a new, efficient, intelligent, and truly open language model created by Snowflake AI Research. Ask me anything."
    st.session_state.messages = [{"role": "assistant", "content": greeting}]

@st.cache_resource(show_spinner=False)
def get_tokenizer():
    """Get a tokenizer to make sure we're not sending too much text
    text to the Model. Eventually we will replace this with ArcticTokenizer
    """
    return AutoTokenizer.from_pretrained("huggyllama/llama-7b")

def get_num_tokens(prompt):
    """Get the number of tokens in a given prompt"""
    tokenizer = get_tokenizer()
    tokens = tokenizer.tokenize(prompt)
    return len(tokens)


def generate_arctic_response(system_prompt: str, temperature = None, top_p = None, assistant_greeting = None, history: list[dict] = None):
    temperature = temperature or 0.01
    top_p = top_p or 0.9
    history = history or st.session_state.messages

    prompt = [f'''<|im_start|>system\n{system_prompt}<|im_end|>''']
    for dict_message in history:
        role = dict_message["role"]
        prompt.append(f"<|im_start|>{role}\n{dict_message['content']}<|im_end|>")
    
    prompt.append("<|im_start|>assistant")
    prompt.append("")
    prompt_str = "\n".join(prompt)
    
    if get_num_tokens(prompt_str) >= 3072:
        st.error("Conversation length too long. Please keep it under 3072 tokens.")
        st.button('Clear chat history', on_click=clear_chat_history, kwargs={"greeting": assistant_greeting}, key="clear_chat_history")
        st.stop()


    input={
        "prompt": prompt_str,
        "prompt_template": r"{prompt}",
        "temperature": temperature,
        "top_p": top_p,
        "stop_sequences": "<|im_end|>"
    }
    snowflake_model = "snowflake/snowflake-arctic-instruct"

    for event in replicate.stream(snowflake_model, input=input):
        yield str(event)
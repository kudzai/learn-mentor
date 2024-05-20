
import streamlit as st
from transformers import AutoTokenizer
from replicate.client import Client

def is_valid_token(token):
    return (token.startswith('r8_') and len(token)==40)

def have_valid_session_token():
    return 'REPLICATE_API_TOKEN' in st.session_state and is_valid_token(st.session_state['REPLICATE_API_TOKEN'])

def show_warning_to_provide_api_token():
    st.write(":warning: :red[**Please provide a token for Replicate API.**]")

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


def generate_arctic_response(system_prompt: str, temperature = None, top_p = None, history: list[dict] = None):
    temperature = temperature or 0.01
    top_p = top_p or 0.9
    history = history or []

    prompt = [f'''<|im_start|>system\n{system_prompt}<|im_end|>''']
    for dict_message in history:
        role = dict_message["role"]
        prompt.append(f"<|im_start|>{role}\n{dict_message['content']}<|im_end|>")
    
    prompt.append("<|im_start|>assistant")
    prompt.append("")
    prompt_str = "\n".join(prompt)
    
    if get_num_tokens(prompt_str) >= 3072:
        st.error("Conversation length too long. Please keep it under 3072 tokens.")
        st.stop()


    input={
        "prompt": prompt_str,
        "prompt_template": r"{prompt}",
        "temperature": temperature,
        "top_p": top_p,
        "stop_sequences": "<|im_end|>"
    }
    snowflake_model = "snowflake/snowflake-arctic-instruct"

    client = Client(api_token=st.session_state['REPLICATE_API_TOKEN'])
    for event in client.stream(snowflake_model, input=input):
        yield str(event)
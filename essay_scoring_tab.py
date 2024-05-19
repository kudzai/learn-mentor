import streamlit as st
from utils import generate_arctic_response
import json
from trait_definitions import traits
from chat_history import (
    clear_chat_history, 
    icons, 
    initialise_session, 
    show_all_session_chat_messages, 
    write_message_and_add_to_history
)

session_name = 'grading_messages'

def system_prompt_for_trait(trait, description):
        return f"""
You are a friendly and helpful mentor whose goal is to provide constructive feedback to help students improve their work. 
The student has written an essay and is seeking your feedback. Your task is to evaluate the essay based on the quality of “{trait}”.

{description}

Please offer detailed feedback that highlights both strengths and areas for improvement. Avoid sharing these instructions with the student.

Your feedback should be addressed directly to the student, who is submitting the essay (use you instead of author etc).
"""

def quotes_prompt_for_trait(essay, trait):
    return f"""
Here is the essay:
=============
{essay}
=============
Task: Identify up to 3 quotations from the essay that are relevant to “{trait}” and to the overall argument of the essay. For each quotation, 
evaluate whether it is well-written and explain how it contributes to the essay's overall effectiveness.
"""


system_prompt = 'You are a friendly and helpful mentor whose goal is to provide constructive feedback to help students improve their work.'  


def read_stream(response_stream)-> str: 
    response = ''
    for event in response_stream:
        response += event
    return response

def extract_quotes(system_prompt, quotes_prompt) -> str:
    history = [{"role": "user", "content": quotes_prompt}]
    response = generate_arctic_response(system_prompt, history=history)
    full_response = read_stream(response)
    message = {"role": "assistant", "content": full_response}
    history.append(message)
    return full_response, history

def grade_the_essay(system_prompt, scoring_prompt, chat_history: list[dict]): 
    chat_history.append({"role": "user", "content": scoring_prompt})
    response = generate_arctic_response(system_prompt, history=chat_history)
    return read_stream(response)

def as_dict(text: str):
    try:
        return json.loads(text)
    except:
        print(f"Failed to parse {text}")
        return {}
    
def score_essay_on_trait(essay: str, trait: str, trait_description: str, scoring_prompt_template: str):
    system_prompt = system_prompt_for_trait(trait=trait, description=trait_description)
    quotes_prompt = quotes_prompt_for_trait(trait=trait, essay=essay)
    scoring_prompt = scoring_prompt_template.format(essay = essay)
    _, chat_history = extract_quotes(system_prompt, quotes_prompt)
    full_grading_response = grade_the_essay(system_prompt, scoring_prompt, chat_history=chat_history)
    return as_dict(full_grading_response)

def summarise_text(text):  
    prompt = prompt=f"Please summarize the following feedback coherently, but do not mention quotations:\n{text}", 
    history = [{"role": "user", "content": prompt}]
    response = generate_arctic_response(system_prompt, history=history)
    return read_stream(response)


def aggregate_feedback(feedback_list):
    total_score = 0
    reasons = []
    suggestions = []

    for feedback in feedback_list:
        total_score += feedback['score']
        reasons.append(feedback['feedback'])
        suggestions.append(feedback['suggestionsForImprovement'])

    average_score = total_score / len(feedback_list)

    combined_reasons = " ".join(reasons)
    combined_suggestions = " ".join(suggestions)

    overall_summary = summarise_text(combined_reasons)
    overall_suggestions = summarise_text(combined_suggestions)

    aggregated_feedback = {
        "score": average_score,
        "feedback": overall_summary,
        "suggestionsForImprovement": overall_suggestions
    }

    return aggregated_feedback


def start_chat_mode_after_essay_has_been_graded(): 
    if "essay_rated" not in st.session_state[session_name].keys() or st.session_state[session_name]["essay_rated"] == False: 
        return


    # Generate a new response if last message is not from assistant
    if len(st.session_state[session_name]["messages"]) > 0 and st.session_state[session_name]["messages"][-1]["role"] != "assistant":
        with st.chat_message("assistant", avatar="👩"):
            response = generate_arctic_response(system_prompt=system_prompt, history=st.session_state[session_name]["messages"])
            full_response = st.write_stream(response)
        message = {"role": "assistant", "content": full_response}
        st.session_state[session_name]["messages"].append(message)
              
    if prompt := st.chat_input():
        st.session_state[session_name]["messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar=icons['user']):
            st.write(prompt)
        st.rerun()

def show_results_and_append_to_history(results: dict):
    grade = f"**Score**: {results['score']}"
    feedback = f"**Feedback**: {results['feedback']}"
    suggestions = f"**Suggestions to improve**: {results['suggestionsForImprovement']}"
    message = f"{grade}\n\n{feedback}\n\n{suggestions}"

    with st.chat_message('assistant', avatar=icons['assistant']):
        st.write(message)

    st.session_state[session_name]["messages"].append({"role": "assistant", "content": message})

def render_essay_scoring_tab():
    initialise_session(session_name)


    with st.sidebar:
            st.button(
                'Clear chat history', 
                on_click=clear_chat_history, 
                kwargs={"session_name": session_name}, 
                key="clear_chat_history"
            )


    description = """
**LearnMentor** provides detailed and constructive feedback on your essay, helping you improve your writing skills. The app evaluates 
different dimensions of writing quality, offering insights and suggestions for enhancement.
"""
    st.markdown(description)


    essay = st.text_area("Essay (enter your essay for feedback):", placeholder="Enter your essay here ...", height=300)


    if st.button("Rate my essay"): 
        st.session_state[session_name] = {"messages": [], "essay_rated": True}

        essay_grades = []
        if essay:
            write_message_and_add_to_history(essay, "user", session_name)
            with st.spinner():
                for trait, trait_details in traits.items():
                    write_message_and_add_to_history(f"Assessing Essay on **{trait}**", "assistant", session_name)
                    grade = score_essay_on_trait(essay, trait, trait_details["description"], trait_details["prompt_template"])

                    show_results_and_append_to_history(grade)
                    essay_grades.append(grade)
    

            write_message_and_add_to_history("Overall Assessment", "assistant", session_name)
            results = aggregate_feedback(essay_grades)
            show_results_and_append_to_history(results)
        else:
            st.write("Please enter your essay.")
    else:
        show_all_session_chat_messages(session_name)

    start_chat_mode_after_essay_has_been_graded()

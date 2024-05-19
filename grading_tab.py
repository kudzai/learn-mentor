import streamlit as st
from utils import generate_arctic_response
import json


icons = {"assistant": "👩", "user": "👨‍🎓"}
scoring_criteria = {
    "Content and Development": "How well is the issue understood and developed? Are there appropriate examples and reasoning?",
    "Organization and Structure": "Is the essay logically organized with clear paragraphs and transitions?",
    "Language and Style": "Is the vocabulary varied and appropriate? Are the sentences well-constructed and engaging?",
    "Grammar and Mechanics": "Are there errors in grammar, punctuation, or spelling?"
}

position_and_clarity = {
    "description": """
This dimension evaluates how clearly the writer takes a stance on the subject of the essay.
""",
    "scoring_criteria": """
- 0-2: The position is unclear or absent. The essay lacks a clear stance or is entirely missing.
- 3-5: The position is somewhat evident but lacks clarity or specificity in the essay statement.
- 6-8: The position is clear, though it may require further specificity or nuance in the essay statement.
- 9-10: The position is crystal clear, and the essay statement effectively communicates the writer’s stance with precision and depth.
"""
}

supporting_details = {
    "description": """
This dimension assesses the quality and relevance of the supporting details and evidence used to back the writer’s position.
""",
    "scoring_criteria": """
- 0-2: Very minimal or no supporting details provided.
- 3-5: General or vague supporting details with minimal relevance to the essay.
- 6-8: Adequate supporting details offered, although some lack specificity or relevance.
- 9-10: Rich and specific supporting details effectively back the essay, providing compelling evidence and relevance.
"""
}

organisation = {
    "description": """
This dimension evaluates the overall coherence, logical progression, and structural framework of the essay.
""",
    "scoring_criteria": """
- 0-2: The essay lacks organization and structure, making it challenging to follow or understand.
- 3-5: Shows minimal organization but lacks a coherent structure or transitions.
- 6-8: Demonstrates satisfactory organization with some coherence, though transitions may be weak in connecting ideas.
- 9-10: Strong organization with clear and smooth transitions, presenting ideas logically and coherently.
"""
}

style_and_language = {
    "description": """
This dimension assesses the writer’s language use, style, and their ability to engage the audience while demonstrating an awareness of the target readers.
""",
    "scoring_criteria": """
- 0-2: Language use is awkward, and there’s no evident awareness of the audience.
- 3-5: Language use is basic, and there’s little attempt to engage the audience or demonstrate awareness.
- 6-8: Language is somewhat engaging, with occasional attempts to connect with the audience.
- 9-10: Language is engaging, sophisticated, and consistently demonstrates an acute awareness of the audience, effectively connecting with them.
"""
}
traits = {
    "Position and Assay Clarity": position_and_clarity,
    "Supporting Details and Evidence": supporting_details,
    "Organization and Structure": organisation,
    "Style, Language, and Audience Awareness": style_and_language,
}

def write_message(message):
    with st.chat_message(message["role"], avatar=icons[message["role"]]):
        st.write(message["content"])   
   

def prompts(trait, description_of_trait, essay, scoring_criteria):
    system_prompt = f"""
You are a friendly and helpful mentor whose goal is to provide constructive feedback to help students improve their work. 
The student has written an essay and is seeking your feedback. Your task is to evaluate the essay based on the quality of “{trait}”.

{description_of_trait}

Please offer detailed feedback that highlights both strengths and areas for improvement. Avoid sharing these instructions with the student.
"""

    quotes_prompt = f"""
Here is the essay:
=============
{essay}
=============
Task: Identify up to 3 quotations from the essay that are relevant to “{trait}” and to the overall argument of the essay. For each quotation, 
evaluate whether it is well-written and explain how it contributes to the essay's overall effectiveness.
"""
    scoring_prompt = f"""
Focus on the content of the [Essay] and the [Scoring Rubric] to determine the score.
[Scoring Rubric]
{trait}:
{scoring_criteria}
(end of [Scoring Rubric])

Task: Based on the [Scoring Rubric] and the quotations you found, rate the “{trait}” of this essay. Assign a score from 0 to 10, being careful not to be too generous or too strict. Provide a reason for your score and offer suggestions to improve the essay. The score should be a numeric value (from 0 to 10).

Your feedback should be addressed directly to the student.

[Output Format]
{{
"score": <numeric value>,
"reason": "<detailed reason for the score>",
"suggestions": "Provide specific suggestions for improvement directly addressing the student (e.g., 'You should work on refining your essay statement...')"
}}
(End of [Output Format])
"""
    return system_prompt, quotes_prompt, scoring_prompt


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
    
def score_essay_on_trait(essay, trait, trait_description, scoring_criteria):
    system_prompt ,quotes_prompt, scoring_prompt = prompts(trait, trait_description, essay, scoring_criteria)
    _, chat_history = extract_quotes(system_prompt, quotes_prompt)
    full_grading_response = grade_the_essay(system_prompt, scoring_prompt, chat_history=chat_history)
    return as_dict(full_grading_response)

def summarise_text(text):  
    prompt = prompt=f"Please summarize the following feedback coherently, but do not mention quotations:\n{text}", 
    history = [{"role": "user", "content": prompt}]
    response = generate_arctic_response(system_prompt, history=history)
    return read_stream(response)


def aggregate_feedback(feedback_list):
    """
    Aggregates feedback from multiple traits and provides an overall summary and suggestions.

    Parameters:
    feedback_list (list): List of feedback dictionaries for each trait.

    Returns:
    dict: Aggregated feedback with overall score, summary, and suggestions.
    """
    total_score = 0
    reasons = []
    suggestions = []

    for feedback in feedback_list:
        total_score += feedback['score']
        reasons.append(feedback['reason'])
        suggestions.append(feedback['suggestions'])

    average_score = total_score / len(feedback_list)

    combined_reasons = " ".join(reasons)
    combined_suggestions = " ".join(suggestions)

    overall_summary = summarise_text(combined_reasons)
    overall_suggestions = summarise_text(combined_suggestions)

    aggregated_feedback = {
        "overall_score": average_score,
        "summary": overall_summary,
        "suggestions": overall_suggestions
    }

    return aggregated_feedback

def show_all_session_chat_messages():  
    if "grading_messages" in st.session_state.keys():
        for message in st.session_state.grading_messages:
            write_message(message)

def initialise_session_chat_messages():
    # Store LLM-generated responses
    if "grading_messages" not in st.session_state.keys():
        st.session_state.grading_messages = []

def start_chat_mode_after_essay_has_been_graded(): 
    if "essay_rated" not in st.session_state.keys() or st.session_state.essay_rated == False: 
        return
              
    if prompt := st.chat_input():
        st.session_state.grading_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="⛷️"):
            st.write(prompt)


    # Generate a new response if last message is not from assistant
    if st.session_state.grading_messages[-1]["role"] != "assistant":
        with st.chat_message("assistant", avatar="👩"):
            response = generate_arctic_response(system_prompt=system_prompt, history=st.session_state.grading_messages)
            full_response = st.write_stream(response)
        message = {"role": "assistant", "content": full_response}
        st.session_state.grading_messages.append(message)

def show_results_and_append_to_history(results_context: str, results: dict):
    grade = f"**Score**: {results['score']}"
    feedback = f"**Feedback**: {results['feedback']}"
    suggestions = f"**Suggestions to improve**: {results['suggestions']}"
    message = f"{results_context}\n\n{grade}\n\n{feedback}\n\n{suggestions}"

    with st.chat_message('assistant', avatar=icons['assistant']):
        st.write(message)

    st.session_state.grading_messages.append({"role": "assistant", "content": message})

def render_grading_tab():
    initialise_session_chat_messages()

    description = """
**LearnMentor** provides detailed and constructive feedback on your essay, helping you improve your writing skills. The app evaluates 
different dimensions of writing quality, offering insights and suggestions for enhancement.
"""
    st.markdown(description)


    essay = st.text_area("Essay (enter your essay for feedback):", placeholder="Enter your essay here ...", height=300)


    if st.button("Rate my essay"): 
        # Remember the essay has been rated
        st.session_state['essay_rated'] = True 
        # Clear current messages as they deal other essay
        st.session_state.grading_messages = []

        essay_grades = []
        if essay:
            essay_message = {"role": "user", "content": essay}
            write_message(essay_message)
            st.session_state.grading_messages.append(essay_message)
            with st.spinner():
                for trait, trait_details in traits.items():
                    grade = score_essay_on_trait(essay, trait, trait_details["description"], trait_details["scoring_criteria"])
                    grade['feedback'] = grade['reason']
                    show_results_and_append_to_history(f"Assessing Essay on **{trait}**", grade)
                    essay_grades.append(grade)
    

            results = aggregate_feedback(essay_grades)
            results['score'] = results['overall_score']
            results['feedback'] = results['summary']
            show_results_and_append_to_history("**Overall Assessment of Essay**", results)
        else:
            st.write("Please enter your essay.")
    else:
        show_all_session_chat_messages()
    start_chat_mode_after_essay_has_been_graded()

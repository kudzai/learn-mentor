

__critical_thinking_and_analysis = {
    'description': "Assesses the depth and insight of the essay's arguments and analysis",
    'prompt_template': """
[Essay] {essay} (end of [Essay])

[Task]
Please evaluate the essay based on its critical thinking and analysis. Provide a score from 0 to 10, with 0 being the lowest and 10 being the highest. Along with the score, provide detailed feedback on the essay's critical thinking and analysis. Additionally, offer suggestions for improvement in this area.

[Scoring Criteria]
- 0-2: Lacks a clear point of view, minimal analysis, superficial or irrelevant arguments.
- 3-5: Some analysis and insight, but arguments may be underdeveloped or inconsistently applied.
- 6-8: Clear point of view with well-developed analysis, though some arguments may lack depth.
- 9-10: Insightful and thorough analysis with strong, well-supported arguments.

[Output Format]
{{
    "score": [Your score here],
    "feedback": "[Detailed feedback on critical thinking and analysis]",
    "suggestionsForImprovement": "[Specific suggestions to improve critical thinking and analysis]"
}}
"""
}
__use_of_evidence = {
    'description': "Measures the relevance and effectiveness of examples, reasons, and evidence used to support the essay's position.",
    'prompt_template': """
[Essay] {essay} (end of [Essay])

[Task]
Please evaluate the essay based on its use of evidence and examples. Provide a score from 0 to 10, with 0 being the lowest and 10 being the highest. Along with the score, provide detailed feedback on the essay's use of evidence and examples. Additionally, offer suggestions for improvement in this area.

[Scoring Criteria]
- 0-2: Inappropriate or insufficient examples, weak support for arguments.
- 3-5: Some relevant examples, but may lack specificity or integration with arguments.
- 6-8: Generally appropriate and well-integrated examples, though some may be less effective.
- 9-10: Highly relevant and effectively integrated examples, providing strong support for arguments.

[Output Format]
{{
    "score": [Your score here],
    "feedback": "[Detailed feedback on use of evidence and examples]",
    "suggestionsForImprovement": "[Specific suggestions to improve use of evidence and examples]"
}}
"""
}
__organisation_and_coherence = {
    'description': "Examines the essay’s structure, clarity, and logical flow of ideas.",
    'prompt_template': """
[Essay] {essay} (end of [Essay])

[Task]
Please evaluate the essay based on its organization and coherence. Provide a score from 0 to 10, with 0 being the lowest and 10 being the highest. Along with the score, provide detailed feedback on the essay's organization and coherence. Additionally, offer suggestions for improvement in this area.

[Scoring Criteria]
- 0-2: Disorganized, unclear structure, difficult to follow.
- 3-5: Some organization, but lacks coherence or has weak transitions.
- 6-8: Generally well-organized with clear progression of ideas, though some parts may be less coherent.
- 9-10: Highly organized, with smooth transitions and clear, logical progression of ideas.

[Output Format]
{{
    "score": [Your score here],
    "feedback": "[Detailed feedback on organization and coherence]",
    "suggestionsForImprovement": "[Specific suggestions to improve organization and coherence]"
}}
"""
}

__language_use_and_mechanics = {
    'description': 'Evaluates the essay’s use of language, vocabulary, grammar, sentence structure, and spelling.',
    'prompt_template': """
[Essay] {essay} (end of [Essay])

[Task]
Please evaluate the essay based on its language use and mechanics, including spelling. Provide a score from 0 to 10, with 0 being the lowest and 10 being the highest. Along with the score, provide detailed feedback on the essay's language use, mechanics, and spelling. Additionally, offer suggestions for improvement in this area.

[Scoring Criteria]
- 0-2: Frequent errors in vocabulary, grammar, mechanics, and spelling, severely affecting readability.
- 3-5: Some errors in language use and spelling, generally understandable with limited complexity and occasional mistakes that do not impede comprehension.
- 6-8: Minor errors in grammar, mechanics, and spelling; generally accurate and varied vocabulary and sentence structures.
- 9-10: Minimal errors in grammar, mechanics, and spelling; varied and sophisticated use of language; accurate and effective vocabulary and sentence structures.

[Output Format]
{{
    "score": [Your score here],
    "feedback": "[Detailed feedback on language use, mechanics, and spelling]",
    "suggestionsForImprovement": "[Specific suggestions to improve language use, mechanics, and spelling]"
}}
"""
}

traits = {
    "Critical Thinking and Analysis": __critical_thinking_and_analysis,
    "Use of Evidence and Examples:": __use_of_evidence,
    "Organization and Coherence": __organisation_and_coherence,
    "Language Use and Mechanics (Including Spelling)": __language_use_and_mechanics,
}
   
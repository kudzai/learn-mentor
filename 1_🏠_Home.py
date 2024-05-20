import streamlit as st
from app_sidebar import app_sidebar


if __name__ == "__main__":
    app_sidebar()

    st.header("Learn Mentor - Your Personal Learning Assistant", divider="rainbow")

    markdown = """
In an ever-evolving educational landscape, Learn Mentor brings the power of generative AI directly to students. 
Designed with accessibility and affordability in mind, our app is built on open-source technology, ensuring that high-quality educational support is
available to all, regardless of internet access.

Recognizing the importance of equitable access to technology, major organizations like UNESCO have emphasized the need for generative AI in education 
to be broadly accessible and inclusive ([Guidance for generative AI in education and research](https://www.unesco.org/en/articles/guidance-generative-ai-education-and-research)). 
Learn Mentor aligns with these principles, striving to bridge the educational divide and provide cutting-edge tools to learners everywhere.

## Key Benefits:
- **Accessibility:** Built to function seamlessly even with limited internet access, Learn Mentor ensures that students everywhere can benefit from cutting-edge AI technology, in line with UNESCO's guidelines on inclusivity.
- **Affordability:** Utilizing open-source resources (e.g., Snowflake's Arctic LLM and Streamlit) allows us to provide top-tier educational tools at a fraction of the cost.
- **Personalization:** Tailored learning experiences adapt to your unique learning style and pace, helping you achieve your academic goals.

## Approach
This was largely influenced by the ideas from a number of sources, including:
- [Student Use Cases for AI](https://hbsp.harvard.edu/inspiring-minds/student-use-cases-for-ai)
- [Prompting Large Language Models for Zero-shot Essay Scoring via Multi-trait Specialization](https://arxiv.org/abs/2404.04941)

It is not a faithful reproduction of those ideas.
"""
    st.markdown(markdown)
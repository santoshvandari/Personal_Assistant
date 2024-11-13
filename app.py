import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain.prompts import PromptTemplate
from langchain.chains import RunnableSequence
from langchain.agents import Tool, initialize_agent, AgentType

# Load environment variables
load_dotenv()

# Configure the Google Generative AI client
genai.configure(api_key=os.getenv("API_KEY"))
genModel = genai.GenerativeModel("gemini-pro")


def get_google_gemini_response(prompt):
    response = genModel.generate_text(
        model="models/text-bison",  # Replace with the correct model ID if needed
        prompt=prompt
    )
    return response.result if response else "No response generated."


class GoogleGeminiRunnable:
    def __call__(self, prompt):
        return get_google_gemini_response(prompt)


def create_email_chain():
    email_prompt = PromptTemplate(
        input_variables=["context"],
        template="Draft a professional email based on the context:\n\n{context}\n\nEmail:"
    )
    return RunnableSequence(email_prompt | GoogleGeminiRunnable())


def initialize_agent_executor():
    tools = [
        Tool(
            name="DraftEmail",
            func=lambda context: create_email_chain().run(context=context),
            description="Draft a professional email based on the context provided."
        ),
        # Add other tools for different tasks here
    ]
    agent = initialize_agent(
        tools=tools,
        llm=GoogleGeminiRunnable(),
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
    )
    return agent


st.title("Personal Assistant with Google Generative AI")

task_type = st.sidebar.selectbox(
    "Select a Task",
    ["Draft Email", "Knowledge-Based Q&A", "Generate Study Plan", "Extract Action Items"]
)

if task_type == "Draft Email":
    st.header("Draft an Email Based on Context")
    context_input = st.text_area("Enter the email context:")
    if st.button("Draft Email"):
        result = create_email_chain().run(context=context_input)
        st.text_area("Generated Email", result, height=300)

elif task_type == "Tool-Using Agent":
    st.header("Tool-Using Agent")
    agent_executor = initialize_agent_executor()
    agent_input = st.text_input("Enter your query (e.g., 'Draft a thank-you email to the team')")
    if st.button("Run Agent"):
        result = agent_executor(agent_input)
        st.text_area("Agent Output", result, height=300)

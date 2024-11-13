import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.agents import Tool, initialize_agent, AgentType

# Load environment variables
load_dotenv()

# Configure the Google Generative AI client
genai.configure(api_key=os.getenv("API_KEY"))
genModel = genai.GenerativeModel("gemini-pro")


def get_google_gemini_response(prompt):
    # Initialize the Google Generative AI client

    # Generate response using Google Gemini
    response = genModel.generate_text(
        model="models/text-bison",  # You can replace with the model ID you prefer
        prompt=prompt
    )

    return response.result if response else "No response generated."

def create_email_chain():
    email_prompt = PromptTemplate(
        input_variables=["context"],
        template="Draft a professional email based on the context:\n\n{context}\n\nEmail:"
    )
    return LLMChain(llm=get_google_gemini_response, prompt=email_prompt)

def initialize_agent_executor():
    tools = [
        Tool(
            name="DraftEmail",
            func=lambda context: create_email_chain().run(context=context),
            description="Draft a professional email based on the context provided."
        ),
        # Add other tools for different tasks here
    ]
    agent = initialize_agent(tools, get_google_gemini_response, agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION)
    return agent
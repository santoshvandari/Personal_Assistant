import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.agents import initialize_agent, Tool, AgentType


# Load environment variables
load_dotenv()

_llm_instance = None

def get_llm_instance():
    global _llm_instance
    if _llm_instance is None:
        # geminiapikey= os.getenv("API_KEY")
        api_key= os.getenv("API_KEY")
        
        if not api_key:
            raise ValueError("API key not found. Please set the API_KEY environment variable.")
        genai.configure(api_key=api_key)
        _llm_instance = genai.GenerativeModel("gemini-pro")
    return _llm_instance



def create_email_chain(llm):
    email_prompt = PromptTemplate(
        input_variables=["context"],
        template="You are drafting a professional email based on the following context:\n\n{context}\n\nProvide the complete email below."
    )
    return LLMChain(llm=llm, prompt=email_prompt)


def create_study_plan_chain(llm):
    study_plan_prompt = PromptTemplate(
        input_variables=["topic", "duration"],
        template="Create a detailed study plan for learning about {topic} over the next {duration}."
    )
    return LLMChain(llm=llm, prompt=study_plan_prompt)


def create_knowledge_qna_chain(llm):
    qna_prompt = PromptTemplate(
        input_variables=["question", "domain"],
        template="Provide a detailed answer to the following question within the context of {domain}:\n\n{question}"
    )
    return LLMChain(llm=llm, prompt=qna_prompt)


def create_action_items_chain(llm):
    action_items_prompt = PromptTemplate(
        input_variables=["notes"],
        template="Extract and list the main action items from the following meeting notes:\n\n{notes}"
    )
    return LLMChain(llm=llm, prompt=action_items_prompt)



def initialize_agent_executor():
    llm = get_llm_instance()
    tools = [
        Tool(
            name="DraftEmail",
            func=lambda context: create_email_chain(llm).run(context=context),
            description="Draft a professional email based on a given context. This tool is specifically for email drafting."
        ),
        Tool(
            name="GenerateStudyPlan",
            func=lambda topic, duration: create_study_plan_chain(llm).run(topic=topic, duration=duration),
            description="Generate a study plan for a topic over a specified duration."
        ),
        Tool(
            name="KnowledgeQnA",
            func=lambda question, domain: create_knowledge_qna_chain(llm).run(question=question, domain=domain),
            description="Answer a question based on a specified knowledge domain."
        ),
        Tool(
            name="ExtractActionItems",
            func=lambda notes: create_action_items_chain(llm).run(notes=notes),
            description="Extract action items from meeting notes."
        )
    ]
   
    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True, return_intermediate_steps=True)
   
    return agent

llm = get_llm_instance()

# Create all chains and the agent executor once to avoid repeated initialization
email_chain = create_email_chain(llm)
study_plan_chain = create_study_plan_chain(llm)
knowledge_qna_chain = create_knowledge_qna_chain(llm)
action_items_chain = create_action_items_chain(llm)
agent_executor = initialize_agent_executor()



st.title("Personal Assistant with LangChain")

task_type = st.sidebar.selectbox("Select a Task", [
    "Draft Email", "Knowledge-Based Q&A",
    "Generate Study Plan", "Extract Action Items", "Tool-Using Agent"
])

if task_type == "Draft Email":
    st.header("Draft an Email Based on Context")
    context_input = st.text_area("Enter the email context:")
    if st.button("Draft Email"):
        result = email_chain.run(context=context_input)
        st.text_area("Generated Email", result, height=300)

elif task_type == "Knowledge-Based Q&A":
    st.header("Knowledge-Based Question Answering")
    domain_input = st.text_input("Enter the knowledge domain (e.g., Finance, Technology, Health):")
    question_input = st.text_area("Enter your question:")
    if st.button("Get Answer"):
        result = knowledge_qna_chain.run(question=question_input, domain=domain_input)
        st.text_area("Answer", result, height=300)

elif task_type == "Generate Study Plan":
    st.header("Generate a Personalized Study Plan")
    topic_input = st.text_input("Enter the topic to study:")
    duration_input = st.text_input("Enter the duration (e.g., 2 weeks, 1 month):")
    if st.button("Generate Study Plan"):
        result = study_plan_chain.run(topic=topic_input, duration=duration_input)
        st.text_area("Study Plan", result, height=300)

elif task_type == "Extract Action Items":
    st.header("Extract Action Items from Meeting Notes")
    notes_input = st.text_area("Enter meeting notes:")
    if st.button("Extract Action Items"):
        result = action_items_chain.run(notes=notes_input)
        st.text_area("Action Items", result, height=300)

elif task_type == "Tool-Using Agent":
    st.header("Tool-Using Agent")
    agent_input = st.text_input("Enter your query (e.g., 'Draft an email thanking the team for their hard work'): ")
   
    if st.button("Run Agent"):
        try:
            execution_results = agent_executor(agent_input)
           
            if isinstance(execution_results, dict) and 'intermediate_steps' in execution_results and execution_results['intermediate_steps']:
                final_result = execution_results['intermediate_steps'][-1][1]  
            else:
                final_result = execution_results.get('output', 'No meaningful output was generated by the agent.')

            st.text_area("Agent Output", final_result, height=300)
       
        except Exception as e:
            st.error(f"An error occurred while running the agent: {str(e)}")
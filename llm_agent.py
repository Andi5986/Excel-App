import os
import pandas as pd
from langchain.agents import create_csv_agent
from langchain.llms import OpenAI
import streamlit as st
from data_processing import process_dataframe

def set_openai_key(api_key):
    os.environ["OPENAI_API_KEY"] = api_key

@st.cache_data
def convert_and_save_as_csv(uploaded_file):
    df = pd.read_excel(uploaded_file)
    df = process_dataframe(df)
    csv_file_path = os.path.abspath('temp.csv')
    df.to_csv(csv_file_path, index=False)
    return csv_file_path

@st.cache_data
def load_data(uploaded_file):
    df = pd.read_excel(uploaded_file)
    df.to_csv('temp.csv', index=False) 
    return 'temp.csv'

@st.cache_data
def create_agent(q):
    agent = create_csv_agent(OpenAI(temperature=0), './temp.csv', verbose=True)
    return agent

@st.cache_data
def get_agent_response(agent, user_input):
    context = """ The dataset is a trial balance."""
    response = agent.run(user_input)
    return response

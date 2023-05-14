import os
import pandas as pd
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI

def set_openai_key(api_key):
    os.environ["OPENAI_API_KEY"] = api_key
    return api_key

def init_agent(api_key):
    api_key = set_openai_key(api_key)
    llm = OpenAI(api_token=api_key)
    pandas_ai = PandasAI(llm, conversational=False)
    return pandas_ai

def get_agent_response(agent, df, user_input):
    response = agent.run(df, user_input)
    return response
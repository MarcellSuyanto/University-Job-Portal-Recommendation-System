import os
from urllib import response
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import pandas as pd
from recom import *


def set_up_chat(df: pd.DataFrame, MODEL='deepseek/deepseek-r1:free'):
    load_dotenv()
    API_KEY = os.getenv("OPENROUTER_KEY")
    llm = ChatOpenAI(
        model=MODEL,
        base_url="https://openrouter.ai/api/v1",
        temperature=0.7,
        api_key=API_KEY
    )
    prompt_template = PromptTemplate(
        input_variables=["job_title", "skills", "industry", "job_listings"],
        template="""
        You are a job recommendation engine. Given the following information:
        Job Title: {job_title}
        Skills: {skills}
        Industry: {industry}
        Job Listings: {job_listings}

        Please provide a list of recommended jobs for the user.
        """
    )
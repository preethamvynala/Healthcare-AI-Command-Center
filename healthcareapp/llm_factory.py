import os
from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_groq import ChatGroq



def get_llm():


    provider=os.getenv(
        "LLM_PROVIDER",
        "groq"
    )


    if provider=="openai":

        return ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0
        )


    elif provider=="gemini":

        return ChatGoogleGenerativeAI(

            model="gemini-2.0-flash",

            temperature=0

        )


    elif provider=="groq":

        return ChatGroq(

            model="llama-3.3-70b-versatile",

            temperature=0

        )


    else:

        raise Exception(
            "Invalid LLM provider"
        )
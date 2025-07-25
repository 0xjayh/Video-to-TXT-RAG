import os
import openai
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv("theEngine/OPENAI_API_KEY.env")

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)
import os
import glob
import openai
import yt_dlp as youtube_dl
from yt_dlp import DownloadError
import docarray
from openai import OpenAI
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
import tiktoken
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_openai import OpenAIEmbeddings

###############################
from theEngine import llm_client
import base64

client = llm_client.client

def generateResponse(youtube_url, query):

    url_to_encode = youtube_url.encode('utf-8')
    encoded_url = base64.b16encode(url_to_encode)
    print(f"Encoded Url is: {encoded_url}")

    output_file = f"file/transcript/{encoded_url}.txt"
    # Import the Text Loader module from langchain
    from langchain_community.document_loaders import TextLoader

    # load the txt file into the loader
    loader = TextLoader(output_file)

    # Load the file into doc
    docs = loader.load()

    # Import the Tiktoken package
    # from langchain_community.document_loaders import TextLoader
    # import tiktoken
    #
    # from langchain.chains import RetrievalQA
    # from langchain_openai import ChatOpenAI
    # from langchain_community.vectorstores import DocArrayInMemorySearch
    # from langchain_openai import OpenAIEmbeddings

    db = DocArrayInMemorySearch.from_documents(
        docs,
        OpenAIEmbeddings()
    )

    retriever = db.as_retriever()

    llm = ChatOpenAI(temperature=0.0)

    qa_stuff = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        verbose=True
    )

    # query = "What is this video about in 25 words?"

    response = qa_stuff.invoke(query)

    print(response)

    return response

#generateResponse("https://www.youtube.com/watch?v=5hPtU8Jbpg0","What is the summary?")
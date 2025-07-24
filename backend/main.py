import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from typing import Union
from theEngine import transcription
from theEngine import rag_process


class Url(BaseModel):
    link: str

class Transcription(BaseModel):
    transcript: str

class AskQuestions(BaseModel):
    link: str
    prompt: str

class AIResponse(BaseModel):
    query: str
    result: str

app = FastAPI()

origins = [
    "http://localhost:5173", 'http://localhost:5173'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
@app.post("/youtube", response_model=Transcription)
def get_url(url: Url):
    link = url.link
    youtube = {"transcript" : link}
    youtube_url = youtube["transcript"]
    # global_url = rag_process.url_encoding(youtube_url)
    transcript_dict = transcription.transcribe_audio(youtube_url)
    # transcript=transcript_dict['transcript']
    # transcript={"transcript": transcript}
    return transcript_dict

@app.post("/ragquestions", response_model=AIResponse)
def ask_questions( question: AskQuestions):
    response = rag_process.generateResponse(question.link, question.prompt)
    #response = rag_process.qa_stuff.invoke(question.prompt)
    print(response)

    return response

@app.get("/")
def read_root():
    return {"Hello": "World"}
# #if name == "main":
# #    uvicorn.run(app, host="0.0.0.0", port=8000)
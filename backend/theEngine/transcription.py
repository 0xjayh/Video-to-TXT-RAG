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
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_openai import OpenAIEmbeddings
import base64
from theEngine import llm_client

client = llm_client.client

# def url_encoding(youtube_url):
#     url_to_encode = youtube_url.encode('utf-8')
#     encoded_url = base64.b16encode(url_to_encode)
#     print(f"Encoded Url is: {encoded_url}")
#     global output_file
#     output_file = (f"file/transcript/{encoded_url}.txt")
#     return output_file

#output_txt_file = output_file
def transcribe_audio(youtube_url):
    # Directory to save audio files
    output_dirs = "file/audio/"

    url_to_encode = youtube_url.encode('utf-8')
    encoded_url = base64.b16encode(url_to_encode)
    print(f"Encoded Url is: {encoded_url}")


    # fileName = youtube_url.split("/")[-1]
    # print(fileName)

    # config for youtube_dl
    
    ydl_config = {
        "format": "best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "outtmpl": os.path.join(output_dirs, f"{encoded_url}.%(ext)s"),
        "verbose": True
    }

    filename = ""

    # Check if the output directory exists and create one if it doesn't
    if not os.path.exists(output_dirs):
        os.makedirs(output_dirs)

    # Indicate which video is being downloaded
    print(f"Downloading video from {youtube_url}")

    print(f"Downloading video from {encoded_url}")

    #Attempt to download the video from the given url, if it fails, then redownload it.
    try:
        with youtube_dl.YoutubeDL(ydl_config) as ydl:
            ydl.download([youtube_url])

    except DownloadError:
        with youtube_dl.YoutubeDL(ydl_config) as ydl:
            ydl.download([youtube_url])

    #search for the audio file in the output directory
    audio_file = glob.glob(os.path.join(output_dirs, "*.mp3"))

    #Select the first audio file names
    refined_file = f"{output_dirs}{encoded_url}.mp3"
    index = audio_file.index(refined_file)

    print(f"Audio file index is {index}")

    audio_filename = audio_file[index]

    print(audio_filename)

    # Audio filename
    audio_file = audio_filename



    output_file = f"file/transcript/{encoded_url}.txt"

    print(output_file)
    model = "whisper-1"

        #Transcribing Audio to Text using the OpenAI API
    print("Converting audio to text using the OpenAI API")

    with open(audio_file, "rb") as audio:
        response = client.audio.transcriptions.create(file=audio, model="whisper-1")

        # Extract the transcript from the response
    print(response)
    transcribed_text = (response.text)
    print(transcribed_text)
    transcript_dict = {"transcript": transcribed_text}
    print(transcript_dict)


    if output_file is not None:
        # Create the directory for the output file if it doesn't exist.
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w") as file:
            file.write(transcribed_text)


    return transcript_dict


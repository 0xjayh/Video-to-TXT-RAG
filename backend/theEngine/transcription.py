import os
import glob
import openai
import yt_dlp as youtube_dl
from yt_dlp import DownloadError
import docarray
from openai import OpenAI
import base64
from theEngine import llm_client

client = llm_client.client

#Function to transcribe the audio from a url
def transcribe_audio(youtube_url):

    # Directory to save audio files
    output_dirs = "file/audio/"

    #Encode the url to have a unique identifier
    url_to_encode = youtube_url.encode('utf-8')
    encoded_url = base64.b16encode(url_to_encode)
    print(f"Encoded Url is: {encoded_url}")

    #Configuration for youtube_dl
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

    #Select the index of the audio file name using the youtube url
    refined_file = f"{output_dirs}{encoded_url}.mp3"
    index = audio_file.index(refined_file)
    print(f"Audio file index is {index}")

    #Pass the unique identifier of the audio file to audio_filename using its index
    audio_filename = audio_file[index]

    print(audio_filename)

    # Audio filename
    audio_file = audio_filename

    #Initialize the name of the transcript file using the same encoded identifier
    output_file = f"file/transcript/{encoded_url}.txt"

    print(output_file)


    #Transcribing Audio to Text using the OpenAI API
    print("Converting audio to text using the OpenAI API")

    #Open the audio file and upload to the whisper-1 transcription model
    with open(audio_file, "rb") as audio:
        response = client.audio.transcriptions.create(file=audio, model="whisper-1")

    # Extract the transcript from the response
    print(response)
    transcribed_text = (response.text)
    print(transcribed_text)
    transcript_dict = {"transcript": transcribed_text}
    print(transcript_dict)

    # Create the directory for the output file if it doesn't exist.
    if output_file is not None:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w") as file:
            file.write(transcribed_text)


    #Return transcript_dict for the FastAPI script to work with
    return transcript_dict


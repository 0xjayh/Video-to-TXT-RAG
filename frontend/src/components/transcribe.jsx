import React from "react";
import Axios from "axios";
import {useEffect, useState} from "react";
import RagPull from "./rag.jsx";

import api from '../api';

function Transcribe() {

    const[videoLink, setVideoLink] = useState("");
    const[transcript, setTranscript] = useState(null);

    const [query, setQuery] = useState("");
    const [generatedResponse, setGeneratedResponse] = useState(null);

    const pullVideo = {
        link: videoLink
    }

    const pullRag = {
        //result: result
        link: videoLink,
        prompt: query
    }

    const fetchTranscript = () => {
        api.post('/youtube', pullVideo).then((res)=> {
           setTranscript(res.data);
           console.log(res.data);
           console.log(pullVideo)
        });
    };

    const fetchData = () => {
        api.post('/ragquestions', pullRag).then((res) => {
            setGeneratedResponse(res.data);
            console.log(res.data);
            console.log(pullRag);
        });
    };

    return(
        <div>
            <h3>Enter URL to transcribe</h3>
            <input
                placeholder="Insert Url"
                onChange={(event) => {
                    setVideoLink(event.target.value);
                }}
                className="video-input"
            />
            <p></p>
            <button onClick={fetchTranscript} className="button"> Transcribe Video </button>
            <p> <b> Transcript </b>: {transcript?.transcript}</p>
            <p></p>

            <h3>Ask questions about your video: 👇🏾</h3>
            <input
                placeholder="What will you like to ask?"
                onChange={(event) => {
                    setQuery(event.target.value);
                }}
                className="query-input"
            />
            <p></p>
            <button onClick={fetchData} className="button"> Refine Content </button>
            <p> <b> Question </b>: {generatedResponse?.query}</p>
            <p> <b> Response </b>: {generatedResponse?.result}</p>

        </div>

    );

}



export default Transcribe;
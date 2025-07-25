import React from "react";
import './App.css';
import Axios from "axios";
import {useEffect, useState} from "react";

function App() {
    const [query, setQuery] = useState("");
    const [GeneratedResponse, setGeneratedResponse] = useState(null)

    const pull_rag = {
        //result: result,
        prompt: query
    }

    const fetchData = () => {
        Axios.post('http://127.0.0.1:8000/ragquestions', pull_rag).then((res) => {
            setGeneratedResponse(res.data);
            console.log(res.data);
            console.log(pull_rag);
        });
    };

    return(
        <div className="App">

            <h1>Hello, convert your Youtube videos to Text here</h1>
            <h1>And ask questions😉</h1>
            <h2>Ask a question</h2>
            <input
                placeholder="What will you like to ask?"
                onChange={(event) => {
                    setQuery(event.target.value);
                }}
            />
            <p></p>
            <button onClick={fetchData}> Refine content </button>
            <h1> Your video says:  </h1>
            <h2>Question: {GeneratedResponse?.query}</h2>
            <h2>Response: {GeneratedResponse?.result}</h2>

        </div>

    );
}

export default App;
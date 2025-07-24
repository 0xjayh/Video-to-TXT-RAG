import React from "react";
import './App.css';
import Axios from "axios";
import {useEffect, useState} from "react";
import "./App.css";
import Transcribe from "./components/transcribe.jsx";

const App = () => {
  return (
    <div className="App">
      <header className="App-header">
          <h2>Hi there, convert Youtube videos to Text here <br/> And ask questions relating to the video😉</h2>
      </header>
      <main>
        <Transcribe />
      </main>
    </div>
  );
};

export default App;
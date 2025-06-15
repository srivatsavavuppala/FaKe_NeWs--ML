import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function FakeNewsChecker() {
  const [text, setText] = useState('');
  const [prediction, setPrediction] = useState('');
  const [explanation, setExplanation] = useState('');

  const checkNews = async () => {
    setPrediction('');
    setExplanation('');
    try {
      const res = await axios.post('http://localhost:8000/predict', { text });
      setPrediction(res.data.prediction);
    } catch (e) {
      setPrediction('Error: Could not connect to backend.');
    }
  };

  const getExplanation = async () => {
    setExplanation('');
    try {
      const res = await axios.post('http://localhost:8000/explain', { text });
      setExplanation(res.data.explanation);
    } catch (e) {
      setExplanation('Error: Could not connect to backend.');
    }
  };

  return (
    <div className="fake-news-container">
      <h2>Fake News Detector</h2>
      <textarea
        rows={6}
        value={text}
        onChange={e => setText(e.target.value)}
        placeholder="Paste news text here..."
      />
      <div>
        <button onClick={checkNews}>Check News</button>
        <button onClick={getExplanation}>Explain</button>
      </div>
      {prediction && <div className="result">Prediction: {prediction}</div>}
      {explanation && <div className="explanation">AI Explanation: {explanation}</div>}
    </div>
  );
}

export default FakeNewsChecker;
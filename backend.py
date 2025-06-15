from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv(dotenv_path="env.vars")
GROQ_API_KEY = os.environ.get("API_KEY")

# Load ML model and vectorizer
MODEL_PATH = "FaKe_NeWs--ML/fake_news_model.pkl"
VECTORIZER_PATH = "FaKe_NeWs--ML/tfidf_vectorizer.pkl"
model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NewsRequest(BaseModel):
    text: str

@app.post("/predict")
def predict_news(news: NewsRequest):
    X = vectorizer.transform([news.text])
    prediction = model.predict(X)[0]
    return {"prediction": prediction}

@app.post("/explain")
def explain_news(news: NewsRequest):
    prompt = f"Explain why the following news is classified as fake or real: {news.text}"
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
        stream=False,
    )
    explanation = chat_completion.choices[0].message.content
    return {"explanation": explanation}

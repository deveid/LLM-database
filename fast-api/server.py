from fastapi import FastAPI
import requests

app = FastAPI()

OLLAMA_URL = "http://ollama:11435"  # Ollama API exposed via Docker container

@app.get("/ask")
def ask_ollama(question: str):
    """Send a question to Ollama and get a response"""
    response = requests.post(
        f"{OLLAMA_URL}/ask", json={"question": question}
    )

    if response.status_code == 200:
        return {"response": response.json()}
    else:
        return {"error": "Ollama service failed", "status_code": response.status_code}


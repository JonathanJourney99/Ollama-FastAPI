from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import ollama
import os

app = FastAPI()


# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)
# Serve index.html
@app.get("/", response_class=HTMLResponse)
def serve_index():
    with open("static/index.html", "r") as file:
        return HTMLResponse(content=file.read())

# Request Model
class PromptRequest(BaseModel):
    userprompt: str

@app.post("/model-generate")
def generate_text(request: PromptRequest):
    resp = ollama.chat(model="qwen2.5:1.5b", messages=[{"role":"user", "content": request.userprompt}])
    return {"resp": resp['message']['content']}

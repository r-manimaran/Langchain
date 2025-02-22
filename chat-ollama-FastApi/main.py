from fastapi import FastAPI, Depends, HTTPException, Header
import ollama
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY_CREDIT = {os.getenv("API_KEY"):5}

app= FastAPI()

def verify_api_key(x_api_key: str = Header(None)):
    credits = API_KEY_CREDIT.get(x_api_key,0)
    print(credits)
    if credits <=0:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    
    return x_api_key

@app.get("/")
def read_root():
    return {"request":"Send request to generate endpoint with prompt"}

@app.post("/generate")
def generate(prompt:str, x_api_key:str= Depends(verify_api_key)):
    API_KEY_CREDIT[x_api_key] -=1
    response = ollama.chat(model='deepseek-r1:7b', messages=[{'role': 'user', 'content': prompt}])
    return {"response":response['message']['content']}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
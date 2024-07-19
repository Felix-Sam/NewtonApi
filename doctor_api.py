import os
import base64
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

# Initialize OpenAI client
MODEL = 'gpt-4o'
client = OpenAI(api_key=os.getenv('CHRISKEY'))

# Initialize FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_methods=['*'],
    allow_credentials=True,
    allow_headers=['*'],
    allow_origins=['*'],
)

def encode_image(image_content):
    return base64.b64encode(image_content).decode("utf-8")

def generate_suggestions(image_base64):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful rice doctor that provides suggestions based on images of rice leaves."},
            {"role": "user", "content": [
                {"type": "text", "text": "Please analyze the condition of this rice leaf."},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/png;base64,{image_base64}"}
                }
            ]}
        ],
        temperature=0.0,
    )
    return response.choices[0].message.content

def rewrite_suggestions(suggestions):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that helps me with my writing."},
            {"role": "user", "content": f"Please rewrite the following suggestions: {suggestions}"}
        ],
        temperature=0.0,
    )
    return response.choices[0].message.content

@app.post("/analyze-rice-leaf")
async def analyze_rice_leaf(file: UploadFile = File(...)):
    try:
        # Read the uploaded file content
        image_content = await file.read()
        image_base64 = encode_image(image_content)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error reading image file")

    # Get suggestions from OpenAI (rice doctor)
    suggestions = generate_suggestions(image_base64)

    # Rewrite suggestions using OpenAI (writing assistant)
    rewritten_suggestions = rewrite_suggestions(suggestions)

    # Return rewritten suggestions as plain text response
    return PlainTextResponse(content=rewritten_suggestions)


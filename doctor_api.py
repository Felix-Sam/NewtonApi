import os
import base64
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
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

class ImageResponse(BaseModel):
    suggestions: str

class ChatbotResponse(BaseModel):
    response: str

class WeatherInsightsResponse(BaseModel):
    insights: str

def encode_image(image_file):
    return base64.b64encode(image_file).decode("utf-8")
    
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

@app.post("/analyze-rice-leaf", response_model=ImageResponse)
async def analyze_rice_leaf(file: UploadFile = File(...)):
    # Read the uploaded file
    image_data = await file.read()
    image_base64 = encode_image(image_data)
    
    # Get suggestions from OpenAI
    suggestions = generate_suggestions(image_base64)
    
    # Return suggestions as JSON response
    return JSONResponse(content={"suggestions": suggestions})

def generate_chatbot_response(user_input):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are an agriculture expert chatbot that provides advice and information to farmers only. Don't respond to anything outside the context of Agriculture."},
            {"role": "user", "content": user_input}
        ],
        temperature=0.0,
    )
    return response.choices[0].message.content

@app.post("/agriculture-chatbot", response_model=ChatbotResponse)
async def agriculture_chatbot(query: str = Form(...)):
    # Get chatbot response from OpenAI
    chatbot_response = generate_chatbot_response(query)
    
    # Return chatbot response as JSON response
    return JSONResponse(content={"response": chatbot_response})

def generate_overall_recommendation(temperature, humidity, windspeed, pressure):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are an agriculture expert that provides overall recommendations for rice farmers based on weather data."},
            {"role": "user", "content": f"The current weather conditions are: Temperature: {temperature}°C, Humidity: {humidity}%, Wind Speed: {windspeed} m/s, Pressure: {pressure} hPa."}
        ],
        temperature=0.0,
    )
    return response.choices[0].message.content

def generate_humidity_recommendation(humidity):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are an agriculture expert that provides recommendations based on humidity for rice farmers."},
            {"role": "user", "content": f"The current humidity level is {humidity}%."}
        ],
        temperature=0.0,
    )
    return response.choices[0].message.content

def generate_pressure_recommendation(pressure):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are an agriculture expert that provides recommendations based on atmospheric pressure for rice farmers."},
            {"role": "user", "content": f"The current pressure is {pressure} hPa."}
        ],
        temperature=0.0,
    )
    return response.choices[0].message.content

def generate_temperature_recommendation(temperature):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are an agriculture expert that provides recommendations based on temperature for rice farmers."},
            {"role": "user", "content": f"The current temperature is {temperature}°C."}
        ],
        temperature=0.0,
    )
    return response.choices[0].message.content

def generate_windspeed_recommendation(windspeed):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are an agriculture expert that provides recommendations based on windspeed for rice farmers."},
            {"role": "user", "content": f"The current windspeed is {windspeed} m/s."}
        ],
        temperature=0.0,
    )
    return response.choices[0].message.content

def generate_spraying_or_fertilizer_advice(temperature, humidity, windspeed, pressure):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are an agriculture expert that advises rice farmers on whether it is a good time for spraying or applying fertilizer based on weather conditions."},
            {"role": "user", "content": f"The current weather conditions are: Temperature: {temperature}°C, Humidity: {humidity}%, Wind Speed: {windspeed} m/s, Pressure: {pressure} hPa. Please advise if it is a good time for spraying or applying fertilizer."}
        ],
        temperature=0.0,
    )
    return response.choices[0].message.content

@app.post("/overall-recommendation", response_model=WeatherInsightsResponse)
async def overall_recommendation(
    temperature: float = Form(...),
    humidity: float = Form(...),
    windspeed: float = Form(...),
    pressure: float = Form(...)
):
    insights = generate_overall_recommendation(temperature, humidity, windspeed, pressure)
    return JSONResponse(content={"insights": insights})

@app.post("/humidity-recommendation", response_model=WeatherInsightsResponse)
async def humidity_recommendation(humidity: float = Form(...)):
    insights = generate_humidity_recommendation(humidity)
    return JSONResponse(content={"insights": insights})

@app.post("/pressure-recommendation", response_model=WeatherInsightsResponse)
async def pressure_recommendation(pressure: float = Form(...)):
    insights = generate_pressure_recommendation(pressure)
    return JSONResponse(content={"insights": insights})

@app.post("/temperature-recommendation", response_model=WeatherInsightsResponse)
async def temperature_recommendation(temperature: float = Form(...)):
    insights = generate_temperature_recommendation(temperature)
    return JSONResponse(content={"insights": insights})

@app.post("/windspeed-recommendation", response_model=WeatherInsightsResponse)
async def windspeed_recommendation(windspeed: float = Form(...)):
    insights = generate_windspeed_recommendation(windspeed)
    return JSONResponse(content={"insights": insights})

@app.post("/spraying-or-fertilizer-advice", response_model=WeatherInsightsResponse)
async def spraying_or_fertilizer_advice(
    temperature: float = Form(...),
    humidity: float = Form(...),
    windspeed: float = Form(...),
    pressure: float = Form(...)
):
    insights = generate_spraying_or_fertilizer_advice(temperature, humidity, windspeed, pressure)
    return JSONResponse(content={"insights": insights})








# Version Two''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# import os
# import base64
# from fastapi import FastAPI, File, UploadFile, Form
# from fastapi.responses import JSONResponse
# from pydantic import BaseModel
# from openai import OpenAI
# from dotenv import load_dotenv
# from fastapi.middleware.cors import CORSMiddleware

# # Load environment variables
# load_dotenv()

# # Initialize OpenAI client
# MODEL = 'gpt-4o'
# client = OpenAI(api_key=os.getenv('CHRISKEY'))

# # Initialize FastAPI app
# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_methods=['*'],
#     allow_credentials=True,
#     allow_headers=['*'],
#     allow_origins=['*'],
# )

# class ImageResponse(BaseModel):
#     suggestions: str

# class ChatbotResponse(BaseModel):
#     response: str

# class WeatherInsightsResponse(BaseModel):
#     insights: str

# def encode_image(image_file):
#     return base64.b64encode(image_file).decode("utf-8")
    
# def generate_suggestions(image_base64):
#     response = client.chat.completions.create(
#         model=MODEL,
#         messages=[
#             {"role": "system", "content": "You are a helpful rice doctor that provides suggestions based on images of rice leaves."},
#             {"role": "user", "content": [
#                 {"type": "text", "text": "Please analyze the condition of this rice leaf."},
#                 {"type": "image_url", "image_url": {
#                     "url": f"data:image/png;base64,{image_base64}"}
#                 }
#             ]}
#         ],
#         temperature=0.0,
#     )
#     return response.choices[0].message.content

# @app.post("/analyze-rice-leaf", response_model=ImageResponse)
# async def analyze_rice_leaf(file: UploadFile = File(...)):
#     # Read the uploaded file
#     image_data = await file.read()
#     image_base64 = encode_image(image_data)
    
#     # Get suggestions from OpenAI
#     suggestions = generate_suggestions(image_base64)
    
#     # Return suggestions as JSON response
#     return JSONResponse(content={"suggestions": suggestions})

# def generate_chatbot_response(user_input):
#     response = client.chat.completions.create(
#         model=MODEL,
#         messages=[
#             {"role": "system", "content": "You are an agriculture expert chatbot that provides advice and information to farmers only. Don't respond to anything outside the context of Agriculture."},
#             {"role": "user", "content": user_input}
#         ],
#         temperature=0.0,
#     )
#     return response.choices[0].message.content

# @app.post("/agriculture-chatbot", response_model=ChatbotResponse)
# async def agriculture_chatbot(query: str = Form(...)):
#     # Get chatbot response from OpenAI
#     chatbot_response = generate_chatbot_response(query)
    
#     # Return chatbot response as JSON response
#     return JSONResponse(content={"response": chatbot_response})

# def generate_weather_insights(temperature: float, humidity: float, windspeed: float, pressure: float):
#     response = client.chat.completions.create(
#         model=MODEL,
#         messages=[
#             {"role": "system", "content": "You are an agriculture expert that provides weather-based insights and advice to rice farmers based on temperature, humidity, wind speed, and pressure."},
#             {"role": "user", "content": f"The current weather conditions are: Temperature: {temperature}°C, Humidity: {humidity}%, Wind Speed: {windspeed} m/s, Pressure: {pressure} hPa. What advice can you give to the rice farmer based on these conditions?"}
#         ],
#         temperature=0.0,
#     )
#     return response.choices[0].message.content

# @app.post("/weather-insights", response_model=WeatherInsightsResponse)
# async def weather_insights(
#     temperature: float = Form(...),
#     humidity: float = Form(...),
#     windspeed: float = Form(...),
#     pressure: float = Form(...)
# ):
#     # Generate insights based on the provided weather data
#     insights = generate_weather_insights(temperature, humidity, windspeed, pressure)
    
#     # Return insights as JSON response
#     return JSONResponse(content={"insights": insights})























# Version one ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# import os
# import base64
# from fastapi import FastAPI, File, UploadFile, Form
# from fastapi.responses import JSONResponse
# from pydantic import BaseModel
# from openai import OpenAI
# from dotenv import load_dotenv
# from fastapi.middleware.cors import CORSMiddleware

# # Load environment variables
# load_dotenv()

# # Initialize OpenAI client
# MODEL = 'gpt-4o'
# client = OpenAI(api_key=os.getenv('CHRISKEY'))

# # Initialize FastAPI app
# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_methods=['*'],
#     allow_credentials=True,
#     allow_headers=['*'],
#     allow_origins=['*'],
# )

# class ImageResponse(BaseModel):
#     suggestions: str

# class ChatbotResponse(BaseModel):
#     response: str

# def encode_image(image_file):
#     return base64.b64encode(image_file).decode("utf-8")
    
# def generate_suggestions(image_base64):
#     response = client.chat.completions.create(
#         model=MODEL,
#         messages=[
#             {"role": "system", "content": "You are a helpful rice doctor that provides suggestions based on images of rice leaves."},
#             {"role": "user", "content": [
#                 {"type": "text", "text": "Please analyze the condition of this rice leaf."},
#                 {"type": "image_url", "image_url": {
#                     "url": f"data:image/png;base64,{image_base64}"}
#                 }
#             ]}
#         ],
#         temperature=0.0,
#     )
#     return response.choices[0].message.content

# @app.post("/analyze-rice-leaf", response_model=ImageResponse)
# async def analyze_rice_leaf(file: UploadFile = File(...)):
#     # Read the uploaded file
#     image_data = await file.read()
#     image_base64 = encode_image(image_data)
    
#     # Get suggestions from OpenAI
#     suggestions = generate_suggestions(image_base64)
    
#     # Return suggestions as JSON response
#     return JSONResponse(content={"suggestions": suggestions})

# def generate_chatbot_response(user_input):
#     response = client.chat.completions.create(
#         model=MODEL,
#         messages=[
#             {"role": "system", "content": "You are an agriculture expert chatbot that provides advice and information to farmers only. Don't respond to anything outside the context of Agriculture."},
#             {"role": "user", "content": user_input}
#         ],
#         temperature=0.0,
#     )
#     return response.choices[0].message.content

# @app.post("/agriculture-chatbot", response_model=ChatbotResponse)
# async def agriculture_chatbot(query: str = Form(...)):
#     # Get chatbot response from OpenAI
#     chatbot_response = generate_chatbot_response(query)
    
#     # Return chatbot response as JSON response
#     return JSONResponse(content={"response": chatbot_response})

# # Run the FastAPI app with: uvicorn newton_Api:app --reload

import os
import openai
import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
from key import api_key
 
# OpenAI API 키 설정
openai.api_key = api_key
 
client = openai.OpenAI()
image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
 
response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "이 그림에 대해 설명해줘."},
                {
                    "type": "image_url",
                    "image_url": image_url
                }
            ]
        }
    ],
    max_tokens=1000
)
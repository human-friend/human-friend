from fastapi import FastAPI
from google.cloud import storage
from google.oauth2 import service_account
import json
import os
from openai import OpenAI
import requests 
import json 
from dotenv import load_dotenv
import time 
load_dotenv()

client = OpenAI()

app = FastAPI()

def get_history_from_bucket(bucket_data):
    return_str = ''

    return return_str

async def access_google_bucket():
    key_path = ''

    credentials = service_account.Credentials.from_service_account_file(key_path)
    client = storage.Client(credentials=credentials)

    bucket_name = "bucket_name"

    bucket = client.get_bucket(bucket_name)

    blob_name = ""

    blob = bucket.blob(blob_name)

    contents = blob.download_as_text()

    return contents 

async def call_gpt_api(bucket_data):
    system_prompt = "You are an empathetic friend."

    history_context = get_history_from_bucket(bucket_data)
    user_prompt = f"""This is my conversation from the last hour. {history_context}
                        Based on this conversation and what has happened, make some guiding emphathetic remark."""
    

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content

async def call_heygen_api(gpt_response):
    url = 'https://api.heygen.com/v2/video/generate'
    headers = {
        "X-Api-Key": os.environ.get("HEYGEN_KEY"),
        "Content-Type": "application/json"
    }
    payload = {
        "video_inputs": [
            {
                "character": {
                    "type": "avatar",
                    "avatar_id": "Daisy-inskirt-20220818",
                    "avatar_style": "normal"
                },
                "voice": {
                    "type": "text",
                    "input_text": gpt_response,
                    "voice_id": "2d5b0e6cf36f460aa7fc47e3eee4ba54"
                },
                "background": {
                    "type": "color",
                    "value": "#008000"
                }
            }
        ],
        "dimension": {
            "width": 1280,
            "height": 720
        },
        "aspect_ratio": "16:9",
        "test": True
    } 

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}, {response.text}"



@app.post("/generate_video")
async def generate_video(prompt: str):
    bucket_data = await access_google_bucket()

    gpt_response = await call_gpt_api(bucket_data, prompt)

    heygen_json = await call_heygen_api(gpt_response)
    video_id = heygen_json["data"]["video_id"]

    video_status_url = f"https://api.heygen.com/v1/video_status.get?video_id={video_id}"
    headers = {
        "X-Api-Key": os.environ.get("HEYGEN_KEY"),
        "Content-Type": "application/json"
    }
    
    while True:
        response = requests.get(video_status_url, headers=headers)
        status = response.json()["data"]["status"]
        if status == "completed":
            video_url = response.json()["data"]["video_url"]
            thumbnail_url = response.json()["data"]["thumbnail_url"]
            print(
                f"Video generation completed! \nVideo URL: {video_url} \nThumbnail URL: {thumbnail_url}"
            )
            break
        
        elif status == "processing" or status == "pending":
            print("Video is still processing. Checking status...")
            time.sleep(5)  # Sleep for 5 seconds before checking again
            
        elif status == "failed":
            error = response.json()["data"]["error"]
            print(f"Video generation failed. '{error}'")
            break


    return {"video_url": video_url}


if __name__  == "__main__":
    test_gpt_response = "I think that you should consider your fight with your friend. I think that it is not the right thing to do. Maybe try apologizing a bit later."
    
    video_url_dict = generate_video("Hey I think that you can be a little kinder to your friend.")
    video_url = video_url_dict["video_url"]
    video_filename = "generated_video.mp4"
    with open(video_filename, "wb") as video_filename:
        video_content = requests.get(video_url).content 
        video_file.write(video_content)


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
import pdb 
import asyncio 
load_dotenv()

client = OpenAI()

app = FastAPI()

def get_history_from_bucket(bucket_data):
    return bucket_data

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
async def generate_video():
    pdb.set_trace()
    #bucket_data = await access_google_bucket()
    bucket_data = """You seriously took the last slice of pizza? Unbelievable. You always do this!
Oh, give me a break. You were late to the event, as usual. If you were on time, maybe you would've gotten it.
Late? You can't be serious. I was ten minutes late because I was picking up drinks for everyone. Unlike you, who just waltzed in empty-handed.
Yeah, and I didn't ask you to do that. Maybe if you cared more about showing up on time instead of trying to be a hero, you'd have had some pizza.
Oh, right. Because showing up on time and being useless is so much better. You didn't even say thanks for the drinks.
I didn’t say thanks because you threw a fit over a slice of pizza. It’s just food, not the end of the world.
It's not just about the pizza, it's about you always thinking only about yourself. Every. Single. Time.
Oh please, stop being so dramatic. It's a slice of pizza, not some grand betrayal. Get over it.
You know what? Forget it. Next time, I'll let you handle everything. Then we'll see how 'just a slice of pizza' feels when it's you left out.
Fine by me. Maybe then you'll learn to prioritize being on time over playing the martyr. Enjoy your tantrum.
And you enjoy being the selfish jerk everyone sees you as. Nice job living up to it."""

    gpt_response = await call_gpt_api(bucket_data)

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
    
    video_url_dict = asyncio.run(generate_video())
    video_url = video_url_dict["video_url"]
    video_filename = "generated_video.mp4"
    with open(video_filename, "wb") as video_file:
        video_content = requests.get(video_url).content 
        video_file.write(video_content)
    


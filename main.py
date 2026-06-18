# from fastapi import FastAPI
# from fastapi.responses import StreamingResponse
# import requests
# import json

# app = FastAPI()

# @app.get("/ai")
# def stream_ai(prompt: str):
#     url = "http://localhost:11434/api/generate"
    
#     payload = {
#         "model": "llama3.2",
#         "prompt": prompt,
#         "stream": True 
#     }

#     def generate_tokens():
#         response = requests.post(url, json=payload, stream=True)
#         for line in response.iter_lines():
#             if line:
#                 json_data = json.loads(line.decode('utf-8'))
#                 token = json_data.get("response", "")
#                 # স্প্রিং বুটের WebClient যেন সহজে বুঝতে পারে, তাই প্লেইন টেক্সট হিসেবে পাঠানো হচ্ছে
#                 yield token

#     # এই রিটার্ন স্টেটমেন্টটি আপনার আগের কোডে নিচে মিসিং ছিল
#     return StreamingResponse(generate_tokens(), media_type="text/plain") 


from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import requests
import json
import urllib.parse  # ফাইলের একদম উপরে এই ইম্পোর্টটি যুক্ত করুন

app = FastAPI()

@app.get("/ai")
def stream_ai(prompt: str, model: str = "llama3.2"): # ডিফল্ট মডেল llama3.2
    url = "http://localhost:11434/api/generate"
    
    payload = {
        "model": model, # এখানে ড্রপডাউনের সিলেক্টেড মডেলটি বসবে (যেমন: llama3.2, deepseek, mistral)
        "prompt": prompt,
        "stream": True 
    }

    def generate_tokens():
        response = requests.post(url, json=payload, stream=True)
        for line in response.iter_lines():
            if line:
                json_data = json.loads(line.decode('utf-8'))
                token = json_data.get("response", "")
                encoded_token = urllib.parse.quote(token)
                yield f"data: {encoded_token}\n\n"

    return StreamingResponse(generate_tokens(), media_type="text/event-stream")

# # @get এর জায়গায় app.get হবে
# @app.get("/ai")
# def stream_ai(prompt: str):
#     url = "http://localhost:11434/api/generate"
    
#     payload = {
#         "model": "llama3.2",
#         "prompt": prompt,
#         "stream": True 
#     }


#     def generate_tokens():
#         response = requests.post(url, json=payload, stream=True)
#         for line in response.iter_lines():
#             if line:
#                 json_data = json.loads(line.decode('utf-8'))
#                 token = json_data.get("response", "")
                
#                 # পুরো টোকেনটাকে ইউআরএল এনকোড করে ফেলুন (যেমন: " am" হয়ে যাবে "%20am")
#                 encoded_token = urllib.parse.quote(token)
                    
#                 yield f"data: {encoded_token}\n\n"

    # def generate_tokens():
    #     response = requests.post(url, json=payload, stream=True)
    #     for line in response.iter_lines():
    #         if line:
    #             json_data = json.loads(line.decode('utf-8'))
    #             token = json_data.get("response", "")
    #             yield f"data: {token}\n\n"
    #             # yield f"{token}"

    return StreamingResponse(generate_tokens(), media_type="text/event-stream")
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# import os
# from dotenv import load_dotenv
# from contextlib import asynccontextmanager
# import re
# from fastapi.responses import HTMLResponse, JSONResponse
# from fastapi import Form
# from google import genai

# load_dotenv()


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     api_key = os.getenv("GEMNI_API_KEY")
#     if not api_key:
#         raise ValueError("GEMNI_API_KEY environment variable is not set.")
#     client=genai.Client(api_key=api_key)
#     app.state.client = client
#     yield

# app=FastAPI(lifespan=lifespan)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],  # Allow React dev server
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# def markdown_to_html(text):
#     text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
#     text = re.sub(r'<strong>(.*?)</strong>:', r'<h3>\1</h3>', text)
#     lines = text.splitlines()
#     html_lines = []
#     in_list = False
#     for line in lines:
#         if line.strip().startswith('*'):
#             if not in_list:
#                 html_lines.append('<ul>')
#                 in_list = True
#             html_lines.append(f"<li>{line.strip()[1:].strip()}</li>")
#         else:
#             if in_list:
#                 html_lines.append('</ul>')
#                 in_list = False
#             if line.strip():
#                 html_lines.append(f"<p>{line.strip()}</p>")
#     if in_list:
#         html_lines.append('</ul>')
#     return '\n'.join(html_lines)

# @app.post("/generate")
# async def generate(prompt: str = Form(...)):
#     client = app.state.client
#     response = client.models.generate_content(
#         model="gemini-2.0-flash",
#         contents=prompt
#     )
#     raw_text = response.text
#     formatted = markdown_to_html(raw_text)
#     return JSONResponse(content={"html": formatted})


    
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from contextlib import asynccontextmanager
from google import genai
import os
from dotenv import load_dotenv
import re
load_dotenv()

class ChatRequest(BaseModel):
    message: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    api_key = os.getenv("GEMNI_API_KEY")
    if not api_key:
        raise ValueError("Missing GEMINI_API_KEY")
    
    client = genai.Client(api_key=api_key)
    app.state.client = client
    yield
    # No teardown needed unless you're cleaning up other stuff

app = FastAPI(lifespan=lifespan)

# Allow React frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def markdown_to_html(text):
    # Convert bold (**text**) or __text__ to <strong>
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    # Convert headers like **Title:** to <h3>Title</h3>
    text = re.sub(r'<strong>(.*?)</strong>:', r'<h3>\1</h3>', text)
    # Convert bullet points to <ul><li>
    lines = text.splitlines()
    html_lines = []
    in_list = False
    for line in lines:
        if line.strip().startswith('*'):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            html_lines.append(f"<li>{line.strip()[1:].strip()}</li>")
        else:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append(f"<p>{line}</p>")
    if in_list:
        html_lines.append('</ul>')
    return '\n'.join(html_lines)
@app.post("/chat")
async def chat(request: ChatRequest):
    client = app.state.client
    response = client.models.generate_content(
        model="gemini-2.0-flash",  # or "gemini-2.0-flash" for faster replies
        contents=request.message
    )
    raw_text = response.text
    formatted_html = markdown_to_html(raw_text)
    return {"reply": formatted_html}

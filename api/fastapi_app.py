import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 폴더 경로 설정: src 폴더의 agent.py를 가져오기 위한 설정
import sys
import os.path
current_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from src.agent import PerfumeAgent

# Aiagent 인스턴스 생성 (챗봇 기능)
agent = PerfumeAgent()

app = FastAPI(title="Perfume Aiagent API", description="FastAPI 마이크로서비스로 Aiagent를 노출")

# CORS 설정
origins = ["http://localhost:3000", "http://localhost:8000", "http://localhost"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 챗봇 입력 데이터 모델
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    message = request.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="빈 메시지는 허용되지 않습니다.")
    try:
        reply = agent.handle_message(message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"내부 서버 오류: {str(e)}")
    return {"reply": reply}

# 기본 상태 확인 엔드포인트
@app.get("/")
def root():
    return {"message": "Perfume Aiagent FastAPI 서비스가 정상 작동중입니다."}

######################################
# 이미지 생성 API 추가 (예: /generate)#
######################################

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# 입력 데이터 모델: 이미지 생성용
class ImageRequest(BaseModel):
    input_text: str

def create_structured_prompt(data: dict) -> str:
    top = data.get("top_note", {})
    middle = data.get("middle_note", {})
    base = data.get("base_note", {})

    top_name = top.get("name", "unknown")
    top_ratio = top.get("ratio", "unknown")
    middle_name = middle.get("name", "unknown")
    middle_ratio = middle.get("ratio", "unknown")
    base_name = base.get("name", "unknown")
    base_ratio = base.get("ratio", "unknown")

    if isinstance(top_ratio, (int, float)) and isinstance(middle_ratio, (int, float)) and isinstance(base_ratio, (int, float)):
        total = top_ratio + middle_ratio + base_ratio
        ratio_info = f"(Note ratios sum to {total} instead of 100)" if total != 100 else ""
    else:
        ratio_info = ""

    prompt = (
        f"Create an abstract contemporary artwork inspired by a perfume. "
        f"The top note is '{top_name}' at {top_ratio}% intensity, "
        f"the middle note is '{middle_name}' at {middle_ratio}% intensity, "
        f"and the base note is '{base_name}' at {base_ratio}% intensity {ratio_info}. "
        "Use vibrant colors, dynamic textures, and expressive forms to capture the evolving scent."
    )
    return prompt

def create_freeform_prompt(free_text: str) -> str:
    prompt = (
        f"Create an abstract contemporary artwork inspired by the following perfume description: "
        f"'{free_text}'. Use vibrant colors, dynamic textures, and expressive forms to capture its unique essence."
    )
    return prompt

def process_input(input_text: str) -> str:
    try:
        data = json.loads(input_text)
        if all(key in data for key in ["top_note", "middle_note", "base_note"]):
            return create_structured_prompt(data)
        else:
            return create_freeform_prompt(input_text)
    except json.JSONDecodeError:
        return create_freeform_prompt(input_text)

def generate_image(prompt: str) -> str:
    try:
        response = client.images.generate(model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        n=1)
        return response.data[0].url
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image generation failed: {e}")

@app.post("/generate")
async def generate_image_endpoint(request: ImageRequest):
    input_text = request.input_text.strip()
    if not input_text:
        raise HTTPException(status_code=400, detail="Input text cannot be empty")
    prompt = process_input(input_text)
    image_url = generate_image(prompt)
    return {"prompt": prompt, "image_url": image_url}

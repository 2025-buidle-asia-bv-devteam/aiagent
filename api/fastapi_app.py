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

# Aiagent 인스턴스 생성
agent = PerfumeAgent()

app = FastAPI(title="Perfume Aiagent API", description="FastAPI 마이크로서비스로 Aiagent를 노출")

# CORS 설정: 별도의 프론트엔드에서 요청할 경우 허용
origins = ["http://localhost:3000", "http://localhost:8000", "http://localhost"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.get("/")
def root():
    return {"message": "Perfume Aiagent FastAPI 서비스가 정상 작동중입니다."}

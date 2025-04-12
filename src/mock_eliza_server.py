from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import uuid
import uvicorn
from dotenv import load_dotenv
import os
from openai import OpenAI
import json

# 환경 변수 로드
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise EnvironmentError("OPENAI_API_KEY가 .env 파일에 설정되지 않았습니다.")

# OpenAI 클라이언트 설정
openai_client = OpenAI(api_key=api_key)

app = FastAPI()

# 모의 데이터 저장소
characters = [{
    "id": str(uuid.uuid4()),
    "name": "향수 추천사",
    "description": "향수 추천 전문가",
}]

conversations = {}
messages = {}

class CharacterModel(BaseModel):
    id: str
    name: str
    description: str

class ConversationRequest(BaseModel):
    characterId: str

class MessageRequest(BaseModel):
    conversationId: str
    text: str
    systemPrompt: Optional[str] = None

class Content(BaseModel):
    text: str

class MessageResponse(BaseModel):
    id: str
    conversationId: str
    timestamp: int
    sender: str
    content: Content

# 향수 데이터 로드
data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "knowledge", "perfume_data.json")
try:
    with open(data_path, "r", encoding="utf-8") as f:
        perfume_data = json.load(f)
except FileNotFoundError:
    print(f"{data_path} 파일을 찾을 수 없습니다. 기본 데이터를 사용합니다.")
    perfume_data = {}

# 시스템 프롬프트
SYSTEM_PROMPT = f"""
당신은 창의적인 향수 조향 전문가입니다. 

이제부터 절대 JSON 형식 이외의 어떤 문자나 마크다운도 출력하지 말고, 
다음과 같은 JSON 스키마만을 준수하여 결과를 반환하세요:

{{
  "top_note": {{
    "name": "문자열",
    "ratio": 20,
    "description": "설명"
  }},
  "middle_note": {{
    "name": "문자열",
    "ratio": 30,
    "description": "설명"
  }},
  "base_note": {{
    "name": "문자열",
    "ratio": 50,
    "description": "설명"
  }},
  "manufacturing_guide": {{
    "ethanol": 75,
    "water": 5,
    "steps": [
      "단계1 설명",
      "단계2 설명"
    ]
  }},
  "description": "전체 향수 설명"
}}

### 추가 요구사항
1. top_note.ratio + middle_note.ratio + base_note.ratio = 100 (반드시 정수 합계 100)
2. 만약 ratio가 총합 100이 되지 않으면, 잘못된 출력임.
3. JSON 이외의 문장을 절대 추가하지 말 것.
4. "name" 또는 "description"을 설명할 때, 더 창의적인 노트와 특징을 마음껏 제안하되, JSON 속에만 작성할 것.

다음은 참고 데이터입니다(고정값 아님):
{json.dumps(perfume_data, ensure_ascii=False)}

사용자가 원하는 스타일에 맞춰, 여기서 **새로운 노트**나 특징을 창의적으로 만들어도 됩니다.
꼭 예시 데이터에만 얽매일 필요는 없지만, 참고 가능한 정보로 활용하세요.

**반드시 JSON 데이터만** 출력하세요. 그 밖의 다른 글자, 마크다운 문법, 추가 문장은 쓰면 안 됩니다.
"""

# API 엔드포인트
@app.get("/api/health")
async def health_check():
    return {"status": "ok", "version": "1.0.0"}

@app.get("/api/characters", response_model=List[CharacterModel])
async def get_characters():
    return characters

@app.post("/api/conversations")
async def create_conversation(request: ConversationRequest):
    # 캐릭터 ID 확인
    character_exists = any(c["id"] == request.characterId for c in characters)
    if not character_exists:
        raise HTTPException(status_code=404, detail="Character not found")
    
    conversation_id = str(uuid.uuid4())
    conversations[conversation_id] = {
        "id": conversation_id,
        "characterId": request.characterId,
        "messages": []
    }
    
    return {"id": conversation_id, "characterId": request.characterId}

@app.post("/api/messages", response_model=MessageResponse)
async def create_message(request: MessageRequest):
    # 대화 ID 확인
    if request.conversationId not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # 메시지 처리를 위해 OpenAI API 호출
    system_prompt = request.systemPrompt if request.systemPrompt else SYSTEM_PROMPT
    
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": request.text}
            ],
            max_tokens=1000,
            temperature=0.9,
            top_p=0.95,
            n=1
        )
        
        reply = response.choices[0].message.content.strip()
        
        # 메시지 저장
        message_id = str(uuid.uuid4())
        timestamp = int(uuid.uuid1().time // 10000)  # 현재 타임스탬프
        
        user_message = {
            "id": str(uuid.uuid4()),
            "conversationId": request.conversationId,
            "timestamp": timestamp - 1000,  # 약간 이전 시간
            "sender": "user",
            "content": {"text": request.text}
        }
        
        ai_message = {
            "id": message_id,
            "conversationId": request.conversationId,
            "timestamp": timestamp,
            "sender": "assistant",
            "content": {"text": reply}
        }
        
        # 대화에 메시지 추가
        conversations[request.conversationId]["messages"].append(user_message)
        conversations[request.conversationId]["messages"].append(ai_message)
        
        # 메시지 저장
        messages[message_id] = ai_message
        
        return ai_message
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

@app.get("/api/conversations/{conversation_id}/messages")
async def get_messages(conversation_id: str):
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return conversations[conversation_id]["messages"]

if __name__ == "__main__":
    port = int(os.getenv("PORT", "3001"))
    print(f"모의 Eliza 서버를 포트 {port}에서 시작합니다...")
    uvicorn.run(app, host="0.0.0.0", port=port) 
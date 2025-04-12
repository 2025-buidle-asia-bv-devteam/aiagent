import os
import json
import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from typing import Dict, Any, List, Optional

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

# 향수 노트 모델
class PerfumeNote(BaseModel):
    name: str
    ratio: int
    description: str

# 제조 가이드 모델
class ManufacturingGuide(BaseModel):
    ethanol: Optional[int] = None
    water: Optional[int] = None
    steps: List[str]

# 챗봇 응답 데이터 모델 (향수 정보 구조화)
class ChatResponse(BaseModel):
    raw_reply: str  # 원본 텍스트 응답
    structured_data: Optional[Dict[str, Any]] = None  # 구조화된 데이터 (있는 경우)
    top_note: Optional[PerfumeNote] = None
    middle_note: Optional[PerfumeNote] = None
    base_note: Optional[PerfumeNote] = None  # 단일 베이스 노트
    manufacturing_guide: Optional[ManufacturingGuide] = None
    description: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "raw_reply": "{\n  \"top_note\": {\n    \"name\": \"Smoky Bergamot\", \"ratio\": 20, \"description\": \"탁월하고 생동감 있는 베르가못에 스모키한 트위스트를 가미하여 첫 인상을 강렬하고 신선하게 시작합니다.\"\n  },\n  \"middle_note\": {\n    \"name\": \"Cedarwood with Smoky Ember\", \"ratio\": 35, \"description\": \"따뜻하고 건조한 우디 톤에 은은한 연기 향을 더해 깊이와 복잡성을 증가시킵니다.\"\n  },\n  \"base_note\": {\n    \"name\": \"Sandalwood with Resinous Edge\", \"ratio\": 45, \"description\": \"크리미하고 부드러운 샌달우드의 우디 베이스에 레진 노트를 추가하여 장기간 지속되는 깊이를 제공합니다.\"\n  },\n  \"manufacturing_guide\": {\n    \"ethanol\": 68,\n    \"water\": 7,\n    \"steps\": [\n      \"탑 노트의 Smoky Bergamot 오일과 미들 노트의 Cedarwood with Smoky Ember 오일을 68%의 에탄올에 천천히 섞어 균일하게 합니다.\",\n      \"베이스 노트인 Sandalwood with Resinous Edge 오일을 추가하고, 잘 섞이도록 부드럽게 저어줍니다.\",\n      \"증류수를 5-10% 첨가하면서 계속 저어줍니다.\",\n      \"혼합물을 3-4주간 15-20°C의 어두운 곳에서 숙성시킵니다.\",\n      \"커피 필터를 사용하여 침전물을 제거하고 멸균된 유리 용기에 담습니다.\"\n    ]\n  },\n  \"description\": \"이 조합은 스모키하고 우디한 요소들을 중심으로 구성하여 깊이감과 복잡성을 제공합니다.\"\n}",
                "structured_data": {
                    "top_note": {"name": "Smoky Bergamot", "ratio": 20, "description": "탁월하고 생동감 있는 베르가못에 스모키한 트위스트를 가미하여 첫 인상을 강렬하고 신선하게 시작합니다."},
                    "middle_note": {"name": "Cedarwood with Smoky Ember", "ratio": 35, "description": "따뜻하고 건조한 우디 톤에 은은한 연기 향을 더해 깊이와 복잡성을 증가시킵니다."},
                    "base_note": {"name": "Sandalwood with Resinous Edge", "ratio": 45, "description": "크리미하고 부드러운 샌달우드의 우디 베이스에 레진 노트를 추가하여 장기간 지속되는 깊이를 제공합니다."},
                    "manufacturing_guide": {
                        "ethanol": 68,
                        "water": 7,
                        "steps": [
                            "탑 노트의 Smoky Bergamot 오일과 미들 노트의 Cedarwood with Smoky Ember 오일을 68%의 에탄올에 천천히 섞어 균일하게 합니다.",
                            "베이스 노트인 Sandalwood with Resinous Edge 오일을 추가하고, 잘 섞이도록 부드럽게 저어줍니다.",
                            "증류수를 5-10% 첨가하면서 계속 저어줍니다.",
                            "혼합물을 3-4주간 15-20°C의 어두운 곳에서 숙성시킵니다.",
                            "커피 필터를 사용하여 침전물을 제거하고 멸균된 유리 용기에 담습니다."
                        ]
                    },
                    "description": "이 조합은 스모키하고 우디한 요소들을 중심으로 구성하여 깊이감과 복잡성을 제공합니다."
                }
            }
        }

def parse_perfume_reply(reply: str) -> Dict[str, Any]:
    """
    향수 응답 텍스트를 파싱하여 구조화된 데이터로 변환
    """
    result = {"raw_reply": reply}
    
    try:
        # JSON 파싱 시도
        data = json.loads(reply)
        
        # 각 필드 매핑
        if "top_note" in data:
            result["top_note"] = data["top_note"]
            
        if "middle_note" in data:
            result["middle_note"] = data["middle_note"]
            
        if "base_note" in data:
            result["base_note"] = data["base_note"]
            
        if "manufacturing_guide" in data:
            result["manufacturing_guide"] = data["manufacturing_guide"]
            
        if "description" in data:
            result["description"] = data["description"]
            
        return result
    except json.JSONDecodeError as e:
        print(f"JSON 파싱 오류: {str(e)}")
        # 정규식 파싱 시도 (기존 방식)
        try:
            # 탑 노트 추출 (향수 제안 포맷)
            top_note_match = re.search(r'탑 노트:\s*([^(]+)\s*\((\d+)%\)\s*-\s*([^\n]+)', reply)
            if top_note_match:
                result["top_note"] = {
                    "name": top_note_match.group(1).strip(),
                    "ratio": int(top_note_match.group(2)),
                    "description": top_note_match.group(3).strip()
                }
            
            # 미들 노트 추출 (향수 제안 포맷)
            middle_note_match = re.search(r'미들 노트:\s*([^(]+)\s*\((\d+)%\)\s*-\s*([^\n]+)', reply)
            if middle_note_match:
                result["middle_note"] = {
                    "name": middle_note_match.group(1).strip(),
                    "ratio": int(middle_note_match.group(2)),
                    "description": middle_note_match.group(3).strip()
                }
            
            # 베이스 노트 추출 (향수 제안 포맷)
            base_note_match = re.search(r'베이스 노트:\s*([^(]+)\s*\((\d+)%\)\s*-\s*([^\n]+)', reply)
            if base_note_match:
                result["base_note"] = {
                    "name": base_note_match.group(1).strip(),
                    "ratio": int(base_note_match.group(2)),
                    "description": base_note_match.group(3).strip()
                }
            
            # 제조 가이드 추출
            guide = {}
            
            # 제조 과정 추출
            process_section = re.search(r'제조 가이드:(.*?)(?=\n\n|\n설명|\Z)', reply, re.DOTALL)
            if process_section:
                process_text = process_section.group(1).strip()
                process_steps = re.findall(r'\d+\.\s+(.*?)(?:\n|$)', process_text)
                if process_steps:
                    guide["steps"] = [step.strip() for step in process_steps]
                    
                    # 에탄올 비율 추출
                    ethanol_match = re.search(r'(\d+)%의 에탄올', process_text)
                    if ethanol_match:
                        guide["ethanol"] = int(ethanol_match.group(1))
                    
                    # 증류수 비율 추출
                    water_match = re.search(r'증류수를 (\d+)-(\d+)% 첨가', process_text)
                    if water_match:
                        min_water = int(water_match.group(1))
                        max_water = int(water_match.group(2))
                        guide["water"] = (min_water + max_water) // 2  # 평균값 사용
            
            if guide:
                result["manufacturing_guide"] = guide
            
            # 설명 추출
            description_match = re.search(r'설명:(.*?)(?=\n\n|\Z)', reply, re.DOTALL)
            if description_match:
                result["description"] = description_match.group(1).strip()
            
        except Exception as e:
            # 정규식 파싱 실패 시 기본 응답만 반환
            print(f"정규식 파싱 오류: {str(e)}")
    
    return result

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    message = request.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="빈 메시지는 허용되지 않습니다.")
    try:
        reply = agent.handle_message(message)
        
        # 향수 정보 파싱
        parsed_data = parse_perfume_reply(reply)
        
        # 응답 구성
        response = ChatResponse(raw_reply=reply)
        
        # 구조화된 데이터가 있으면 추가
        if len(parsed_data) > 1:  # raw_reply 외에 다른 필드가 있으면
            # 개별 필드 설정
            if "top_note" in parsed_data:
                response.top_note = PerfumeNote(**parsed_data["top_note"])
            
            if "middle_note" in parsed_data:
                response.middle_note = PerfumeNote(**parsed_data["middle_note"])
            
            if "base_note" in parsed_data:
                response.base_note = PerfumeNote(**parsed_data["base_note"])
            
            if "manufacturing_guide" in parsed_data:
                response.manufacturing_guide = ManufacturingGuide(**parsed_data["manufacturing_guide"])
            
            if "description" in parsed_data:
                response.description = parsed_data["description"]
                
            # 구조화된 데이터 설정 (raw_reply 제외)
            structured_data = {k: v for k, v in parsed_data.items() if k != "raw_reply"}
            if structured_data:
                response.structured_data = structured_data
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"내부 서버 오류: {str(e)}")

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

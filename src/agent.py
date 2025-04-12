import os
import json
import requests
from dotenv import load_dotenv
from openai import OpenAI
import time

# 환경 변수 로드 (기존 값 덮어쓰기)
load_dotenv(override=True)
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise EnvironmentError("OPENAI_API_KEY가 .env 파일에 설정되지 않았습니다.")

# Eliza 설정
ELIZA_ENABLED = os.getenv("USE_ELIZA", "false").lower() == "true"
ELIZA_API_URL = os.getenv("ELIZA_API_URL", "http://localhost:3001")

# OpenAI 클라이언트 설정
client = OpenAI(api_key=api_key)

# 향수 데이터 로드
data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "knowledge", "perfume_data.json")
try:
    with open(data_path, "r", encoding="utf-8") as f:
        perfume_data = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError(f"{data_path} 파일을 찾을 수 없습니다. 파일 경로를 확인하세요.")

# SYSTEM_PROMPT 정의 (포맷팅이 필요하면 format을 사용)
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

class ElizaClient:
    """Eliza API와 통신하기 위한 클라이언트 클래스"""
    
    def __init__(self, api_url):
        self.api_url = api_url
        self.conversation_id = None
        self.character_id = None
        
    def initialize_conversation(self):
        """새로운 대화 시작"""
        try:
            # 실제 Eliza 서버는 /api/characters 대신 다른 엔드포인트를 사용할 수 있습니다.
            # 임시로 캐릭터 ID를 직접 설정하고 대화를 시작합니다.
            self.character_id = "default_character_id"
            
            # 실제 Eliza 서버에 맞는 엔드포인트로 대화 시작
            try:
                # 모의 서버 방식 시도
                response = requests.post(
                    f"{self.api_url}/api/conversations", 
                    json={"characterId": self.character_id}
                )
                
                if response.status_code == 200:
                    self.conversation_id = response.json()["id"]
                    return True
            except Exception:
                # 실패 시 두 번째 방법 시도
                pass
                
            # 대체 방법: 직접 대화 세션 생성
            conversation_id = f"conv_{int(time.time())}"
            self.conversation_id = conversation_id
            return True
            
        except Exception as e:
            print(f"Eliza 초기화 오류: {str(e)}")
            return False
    
    def send_message(self, message_text, system_prompt=None):
        """메시지 전송 및 응답 받기"""
        if not self.conversation_id:
            if not self.initialize_conversation():
                return "Eliza 대화를 초기화할 수 없습니다."
        
        try:
            # 모의 서버 방식으로 시도
            try:
                # 메시지 데이터 구성
                message_data = {
                    "text": message_text,
                    "conversationId": self.conversation_id
                }
                
                # 시스템 프롬프트가 있으면 추가
                if system_prompt:
                    message_data["systemPrompt"] = system_prompt
                
                # 메시지 전송
                response = requests.post(
                    f"{self.api_url}/api/messages", 
                    json=message_data
                )
                
                if response.status_code == 200:
                    # 응답 메시지 가져오기
                    response_data = response.json()
                    
                    # 텍스트 응답 반환
                    if "content" in response_data and "text" in response_data["content"]:
                        return response_data["content"]["text"]
            except Exception:
                # 실패 시 다른 방법 시도
                pass
            
            # 실제 Eliza 서버 방식으로 시도 (필요한 경우 수정)
            # 여기에 실제 Eliza 서버에 맞는 요청 코드를 작성
            # 예: API 형식이 다를 수 있음
            
            # 직접 OpenAI API 호출 (대체 방법)
            openai_client = OpenAI(api_key=api_key)
            response = openai_client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message_text}
                ],
                max_tokens=1000,
                temperature=0.9,
                top_p=0.95,
                n=1
            )
            
            return response.choices[0].message.content.strip()
                
        except Exception as e:
            return f"Eliza API 오류: {str(e)}"
            
    def process_openai_response(self, openai_response, user_input):
        """
        OpenAI 응답을 받아서 Eliza가 자체적으로 처리한 후 응답을 반환합니다.
        """
        try:
            # Eliza가 OpenAI 응답을 분석하고 재해석하는 부분
            eliza_prompt = f"""
다음은 OpenAI API가 생성한 향수 조향 전문가의 답변입니다:

{openai_response}

이 응답을 Eliza로서 당신만의 방식으로 재구성하세요. 
JSON 형식은 유지하되, 필요에 따라 일부 값을 수정하거나 개선할 수 있습니다.
더 창의적인 향수 이름이나 설명을 추가하거나, 제조 가이드를 개선할 수 있습니다.
단, 최종 응답은 반드시 유효한 JSON 형식을 유지해야 하며, 
top_note, middle_note, base_note의 비율 합이 정확히 100이 되어야 합니다.

사용자 질문: {user_input}
"""
            # Eliza의 자체 처리를 위한 OpenAI API 호출
            eliza_client = OpenAI(api_key=api_key)
            eliza_response = eliza_client.chat.completions.create(
                model="gpt-3.5-turbo",  # Eliza 처리용으로는 gpt-3.5-turbo 사용
                messages=[
                    {"role": "system", "content": "당신은 Eliza라는 이름의 창의적인 향수 전문가입니다."},
                    {"role": "user", "content": eliza_prompt}
                ],
                max_tokens=1000,
                temperature=1.0,  # 더 높은 창의성
                top_p=0.98,
                n=1
            )
            
            # Eliza가 재구성한 응답 반환
            return eliza_response.choices[0].message.content.strip()
                
        except Exception as e:
            print(f"Eliza의 OpenAI 응답 처리 오류: {str(e)}")
            # 오류 발생 시 원래 OpenAI 응답 그대로 반환
            return openai_response


class PerfumeAgent:
    def __init__(self):
        self.history = []  # 대화 기록
        self.max_history = 20  # 기록 제한
        
        # Eliza 클라이언트 초기화 (활성화된 경우)
        self.eliza_client = None
        if ELIZA_ENABLED:
            try:
                self.eliza_client = ElizaClient(ELIZA_API_URL)
                print("Eliza 인프라를 사용하도록 설정되었습니다.")
            except Exception as e:
                print(f"Eliza 클라이언트 초기화 오류: {str(e)}")
                self.eliza_client = None

    def handle_message(self, user_input):
        if not user_input.strip():
            return "어떤 스타일의 향수를 원하시나요? 예: '스모키하고 어두운'"

        # 항상 먼저 OpenAI API로 기본 응답 생성
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
        ] + self.history + [{"role": "user", "content": user_input}]

        try:
            # OpenAI API를 통해 기본 응답 생성
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=messages,
                max_tokens=1000,
                temperature=0.9,
                top_p=0.95,
                n=1
            )
            openai_reply = response.choices[0].message.content.strip()
            
            # Eliza가 활성화되어 있으면 OpenAI 응답을 Eliza로 처리
            if ELIZA_ENABLED and self.eliza_client:
                try:
                    # Eliza가 OpenAI 응답을 자체적으로 처리
                    final_reply = self.eliza_client.process_openai_response(openai_reply, user_input)
                    reply = final_reply
                    print(f"Eliza 처리 성공: OpenAI 응답을 재해석했습니다.")
                except Exception as e:
                    print(f"Eliza의 OpenAI 응답 처리 중 오류: {str(e)}")
                    # 오류 시 원래 OpenAI 응답 사용
                    reply = openai_reply
            else:
                # Eliza가 비활성화된 경우 원래 OpenAI 응답 사용
                reply = openai_reply
        except Exception as e:
            reply = f"오류 발생: {str(e)}. API 키, 네트워크 상태, 혹은 요청 구성을 확인하세요."

        # 대화 기록 업데이트: 최근 max_history 메시지만 보존
        self.history.append({"role": "user", "content": user_input})
        self.history.append({"role": "assistant", "content": reply})
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

        return reply

import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# 환경 변수 로드
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise EnvironmentError("OPENAI_API_KEY가 .env 파일에 설정되지 않았습니다.")

# OpenAI 클라이언트 설정
client = OpenAI(api_key=api_key)

# 향수 데이터 로드
data_path = os.path.join("knowledge", "perfume_data.json")
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

class PerfumeAgent:
    def __init__(self):
        self.history = []  # 대화 기록
        self.max_history = 20  # 기록 제한

    def handle_message(self, user_input):
        if not user_input.strip():
            return "어떤 스타일의 향수를 원하시나요? 예: '스모키하고 어두운'"

        # 대화 메시지 구성: 시스템 프롬프트 + 대화 기록 + 현재 사용자 입력
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
        ] + self.history + [{"role": "user", "content": user_input}]

        try:
            response = client.chat.completions.create(model="gpt-4-turbo",  # 또는 gpt-3.5-turbo를 테스트하세요.
            messages=messages,
            max_tokens=1000,
            temperature=0.9,
            top_p=0.95,
            n=1)
            reply = response.choices[0].message.content.strip()
        except Exception as e:
            reply = f"오류 발생: {str(e)}. API 키, 네트워크 상태, 혹은 요청 구성을 확인하세요."

        # 대화 기록 업데이트: 최근 max_history 메시지만 보존
        self.history.append({"role": "user", "content": user_input})
        self.history.append({"role": "assistant", "content": reply})
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

        return reply

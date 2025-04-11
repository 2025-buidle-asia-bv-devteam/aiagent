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
당신은 창의적인 향수 조향 전문가입니다. 사용자가 원하는 스타일에 맞춰 다음 데이터를 참고하되, 기존 노트에 얽매이지 않고 새로운 노트와 조합을 제안하세요:

{json.dumps(perfume_data, ensure_ascii=False)}

- 새로운 노트를 만들 때는 독특한 이름과 특징을 첨가하세요.
- 답변 형식은 아래 형식을 따르며, 탑/미들/베이스 노트의 비율 합계가 반드시 100%여야 합니다.
- 제조 가이드는 각 노트의 특성에 따라 에탄올 비율이나 숙성 시간을 조정합니다.
- 예시:
  - 탑 노트: [노트 이름] ([비율]%) - [특징]
  - 미들 노트: [노트 이름] ([비율]%) - [특징]
  - 베이스 노트: [노트 이름] ([비율]%) - [특징]
  - 제조 가이드: [재료 비율 및 제조 과정]
  - 설명: [조합 선택의 이유와 창의적 포인트]
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
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # 또는 gpt-3.5-turbo를 테스트하세요.
                messages=messages,
                max_tokens=600,
                temperature=0.9,
                top_p=0.95,
                n=1
            )
            reply = response.choices[0].message.content.strip()
        except Exception as e:
            reply = f"오류 발생: {str(e)}. API 키, 네트워크 상태, 혹은 요청 구성을 확인하세요."

        # 대화 기록 업데이트: 최근 max_history 메시지만 보존
        self.history.append({"role": "user", "content": user_input})
        self.history.append({"role": "assistant", "content": reply})
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

        return reply

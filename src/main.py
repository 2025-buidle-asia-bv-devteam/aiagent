import os
import json
from agent import PerfumeAgent
from dotenv import load_dotenv

def main():
    """향수 에이전트 실행"""
    # 환경 변수 로드 (기존 값 덮어쓰기)
    load_dotenv(override=True)
    
    # Eliza 설정 확인
    eliza_enabled = os.getenv("USE_ELIZA", "false").lower() == "true"
    if eliza_enabled:
        print("🚀 Eliza 인프라를 사용하여 향수 에이전트를 시작합니다.")
    else:
        print("🚀 OpenAI API를 직접 사용하여 향수 에이전트를 시작합니다.")
    
    # 에이전트 초기화
    agent = PerfumeAgent()
    print("\n==================================================")
    print("🌹 향수 조향 AI에 오신 것을 환영합니다! 🌹")
    print("==================================================")
    print("원하는 향수 스타일을 설명해 주세요.")
    print("종료하려면 'q' 또는 'exit'를 입력하세요.")
    print("--------------------------------------------------")
    
    while True:
        user_input = input("\n🤔 어떤 향수를 원하시나요? > ")
        
        # 종료 조건
        if user_input.lower() in ['q', 'exit', '종료', '나가기']:
            print("👋 향수 에이전트를 종료합니다. 감사합니다!")
            break
        
        # 빈 입력 처리
        if not user_input.strip():
            print("💡 예시: '스모키하고 어두운 분위기의 향수를 만들고 싶어요'")
            continue
        
        # 에이전트 응답 생성
        print("\n⏳ 향수 레시피를 생성 중입니다...")
        response = agent.handle_message(user_input)
        
        # JSON 형식 검증 및 예쁘게 출력
        try:
            # JSON 문자열인지 확인하고 파싱
            json_response = json.loads(response)
            print("\n✨ 향수 레시피가 생성되었습니다!")
            print("--------------------------------------------------")
            # 예쁘게 출력
            formatted_json = json.dumps(json_response, indent=2, ensure_ascii=False)
            print(formatted_json)
            print("--------------------------------------------------")
        except json.JSONDecodeError:
            # JSON이 아닌 경우 그대로 출력
            print(f"\n🔍 생성된 응답:\n{response}")
            
        print("\n다른 향수 스타일을 시도해보시겠어요?")

if __name__ == "__main__":
    main() 
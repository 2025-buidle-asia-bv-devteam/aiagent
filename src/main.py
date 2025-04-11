from agent import PerfumeAgent

def main():
    print("🌸 향수 추천 AI에 오신 것을 환영합니다! 🌸")
    print("원하는 향수 스타일을 말씀해주세요 (예: '스모키하고 어두운').")
    print("종료하려면 'quit' 또는 'exit'을 입력하세요.")

    agent = PerfumeAgent()
    while True:
        user_input = input("당신: ")
        if user_input.lower() in ["quit", "exit"]:
            print("멋진 향수를 만드시길 바랍니다! 안녕히 가세요~")
            break
        response = agent.handle_message(user_input)
        print(f"AI: {response}\n")

if __name__ == "__main__":
    main()

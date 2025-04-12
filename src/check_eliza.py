import requests
import os
from dotenv import load_dotenv
import time
import sys

# 환경 변수 로드를 먼저 실행 (기존 값 덮어쓰기)
load_dotenv(override=True)

# 전역 변수로 Eliza API URL 설정
ELIZA_URL = os.getenv("ELIZA_API_URL", "http://localhost:3001")
print(f"DEBUG: ELIZA_URL = {ELIZA_URL}")

def check_eliza_server(url, max_retries=3, retry_delay=2):
    """Eliza API 서버가 실행 중인지 확인합니다."""
    print(f"Eliza 서버({url}) 연결 테스트 중...")
    
    for i in range(max_retries):
        try:
            response = requests.get(f"{url}/api/health", timeout=5)
            if response.status_code == 200:
                print("✅ Eliza 서버에 성공적으로 연결되었습니다!")
                print(f"응답: {response.json()}")
                return True
            else:
                print(f"❌ Eliza 서버 응답 오류: 상태 코드 {response.status_code}")
        except requests.RequestException as e:
            print(f"❌ 연결 오류 ({i+1}/{max_retries}): {str(e)}")
        
        if i < max_retries - 1:
            print(f"{retry_delay}초 후 재시도...")
            time.sleep(retry_delay)
    
    return False

def check_characters(url):
    """Eliza 서버에서 사용 가능한 캐릭터 목록을 확인합니다."""
    try:
        response = requests.get(f"{url}/api/characters", timeout=5)
        if response.status_code == 200:
            characters = response.json()
            if characters:
                print(f"✅ 사용 가능한 캐릭터: {len(characters)}개")
                for idx, char in enumerate(characters):
                    print(f"  {idx+1}. {char.get('name', 'Unknown')} (ID: {char.get('id', 'Unknown')})")
                return True
            else:
                print("❌ 사용 가능한 캐릭터가 없습니다.")
        else:
            print(f"❌ 캐릭터 목록 가져오기 실패: 상태 코드 {response.status_code}")
    except requests.RequestException as e:
        print(f"❌ 캐릭터 목록 요청 오류: {str(e)}")
    
    return False

def start_eliza_server():
    """Eliza 서버 시작 명령어를 안내합니다."""
    # 전역 변수에서 URL 사용
    port = ELIZA_URL.split(":")[-1]
    
    print("\n📋 Eliza 서버 시작 방법:")
    print("1. 터미널을 열고 프로젝트 루트 디렉토리로 이동")
    print("2. 다음 명령어 실행:")
    print(f"   PORT={port} pnpm start")
    print("\n또는 DirectClient만 실행하려면:")
    print(f"   cd packages/client-direct && PORT={port} pnpm dev")
    print(f"\n⚠️ 참고: Node 서버가 다른 포트를 사용하고 있다면 {port} 포트를 사용해야 합니다.")
    print(f"   현재 설정된 포트: {port} (.env 파일의 ELIZA_API_URL 값)")
    print("\n서버가 실행되면 '.env' 파일에서 USE_ELIZA=true로 설정하세요.")

def main():
    # 환경 변수는 이미 로드됨
    
    print("=" * 50)
    print("Eliza 서버 상태 확인")
    print("=" * 50)
    
    # 서버가 실행 중인지 확인
    server_running = check_eliza_server(ELIZA_URL)
    
    if not server_running:
        print("\n❌ Eliza 서버에 연결할 수 없습니다.")
        start_eliza_server()
        return False
    
    # 캐릭터 확인
    print("\n캐릭터 정보 확인 중...")
    characters_available = check_characters(ELIZA_URL)
    
    if not characters_available:
        print("\n⚠️ 캐릭터를 찾을 수 없습니다. Eliza를 사용하려면 최소 하나의 캐릭터가 필요합니다.")
        print("캐릭터가 설정되었는지 확인하고 다시 시도하세요.")
        return False
    
    print("\n✅ Eliza 시스템이 정상적으로 작동 중입니다.")
    
    # 환경 변수가 설정되어 있는지 확인
    is_eliza_enabled = os.getenv("USE_ELIZA", "false").lower() == "true"
    if not is_eliza_enabled:
        print("\n⚠️ Eliza는 사용 가능하지만 활성화되어 있지 않습니다.")
        print("'.env' 파일에서 USE_ELIZA=true로 설정하여 활성화하세요.")
    else:
        print("\n✅ Eliza가 활성화되어 있습니다.")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
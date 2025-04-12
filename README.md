# 조향 AI agent

Eliza를 사용한 조향 Aiagent입니다.

## 🚩 개요

Eliza와 향수 데이터를 사용하여 GPT API를 사용하여 사용자가 요구하는 느낌의 향수 조합법을 추천합니다.

## 🛠 설치 및 설정

1. 필요한 패키지 설치:
   ```bash
   pip install -r requirements.txt
   ```

2. `.env` 파일 설정:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   
   # Eliza 설정
   USE_ELIZA=false  # Eliza 사용 시 true로 변경
   ELIZA_API_URL=http://localhost:3001  # Node 서버와 포트 충돌을 피하기 위해 3001 사용
   ```

## 🔍 Eliza 통합 설정

이 프로젝트는 세 가지 모드로 실행할 수 있습니다:

### 1. 기본 모드 (OpenAI API 직접 사용)
- OpenAI API를 직접 호출하여 향수 추천을 생성합니다.
- `.env` 파일에서 `USE_ELIZA=false`로 설정합니다.

### 2. 모의 Eliza 서버 모드 (권장)
- 프로젝트에 포함된 모의 Eliza 서버를 사용합니다.
- 실제 Eliza 서버 설정 없이도 Eliza API 형식을 사용할 수 있습니다.

모의 Eliza 서버 모드 활성화 순서:

1. 모의 Eliza 서버 시작:
   ```bash
   python src/mock_eliza_server.py
   ```

2. 다른 터미널에서 서버 실행 상태 확인:
   ```bash
   python src/check_eliza.py
   ```

3. `.env` 파일에서 Eliza 활성화:
   ```
   USE_ELIZA=true
   ```

4. 향수 에이전트 실행:
   ```bash
   python src/main.py
   ```

### 3. 실제 Eliza 서버 모드 (고급)
- 실제 Eliza 인프라를 통해 요청을 처리합니다.
- 고급 기능 및 캐싱, 향상된 로깅 등의 이점이 있습니다.
- Node.js 23.3.0 및 pnpm이 필요합니다.

Eliza 서버 모드 활성화 순서:

1. 필요한 도구 설치:
   ```bash
   npm install -g pnpm
   ```

2. Eliza 서버 시작:
   ```bash
   # 프로젝트 루트 디렉토리에서
   PORT=3001 pnpm start
   
   # 또는 DirectClient만 실행
   cd packages/client-direct && PORT=3001 pnpm dev
   ```

   > ⚠️ **참고**: Node 서버가 이미 3000 포트를 사용 중이므로 3001과 같은 다른 포트를 사용합니다.

3. `.env` 파일에서 Eliza 활성화:
   ```
   USE_ELIZA=true
   ```

## 📝 사용 방법

1. 향수 에이전트 실행:
   ```bash
   python src/main.py
   ```

2. 원하는 향수 스타일에 대한 설명을 입력합니다.
   예: "스모키하고 어두운 느낌의 향수를 만들고 싶어요"

3. AI가 향수 조합법과 제조 가이드를 JSON 형식으로 제공합니다.

## 📚 구성 요소

- `src/agent.py`: 핵심 에이전트 로직 (OpenAI API 및 Eliza 통합)
- `src/mock_eliza_server.py`: 모의 Eliza API 서버
- `src/check_eliza.py`: Eliza 서버 상태 확인 도구
- `src/main.py`: 메인 실행 파일
- `knowledge/perfume_data.json`: 향수 데이터 참고 자료

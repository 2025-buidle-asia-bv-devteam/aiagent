#!/bin/bash

# Node.js 옵션 설정
export NODE_OPTIONS="--experimental-modules --enable-source-maps --no-warnings"

# 포트 설정 (기본값 3001)
PORT=${PORT:-3001}

# Eliza 서버 시작
echo "🚀 Node.js 옵션: $NODE_OPTIONS"
echo "🌐 포트: $PORT"
echo "⏳ Eliza 서버를 시작합니다..."

# 실행
PORT=$PORT pnpm --filter "@elizaos/agent" start --isRoot 
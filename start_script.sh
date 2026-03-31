#!/bin/bash

# 에러 발생 시 스크립트 즉시 중단
set -e

echo "NER API 자동 설정 스크립트를 시작 (도커 기반)"

# 도커 설치 확인
if ! command -v docker &> /dev/null; then
    echo "에러: Docker 설치 필요"
    exit 1
fi

# 없을 경우 models 폴더 생성
mkdir -p models
cd models

# 첫 번째 모델 다운로드 (0.8B)
MODEL_1="Qwen3.5-0.8B-Q4_K_M.gguf"
URL_1="https://huggingface.co/unsloth/Qwen3.5-0.8B-GGUF/resolve/main/Qwen3.5-0.8B-Q4_K_M.gguf"

# 파일이 이미 존재하는지 검사해서 중복 다운로드 방지
if [ ! -f "$MODEL_1" ]; then
    echo "$MODEL_1 모델 다운로드 중"
    curl -L "$URL_1" -o "$MODEL_1"
else
    echo "$MODEL_1 파일이 이미 존재함. 다운로드 셍략"
fi

# 두 번째 모델 다운로드 (2B)
MODEL_2="Qwen3.5-2B-Q4_K_M.gguf"
URL_2="https://huggingface.co/unsloth/Qwen3.5-2B-GGUF/resolve/main/Qwen3.5-2B-Q4_K_M.gguf"

if [ ! -f "$MODEL_2" ]; then
    echo "$MODEL_2 모델 다운로드 중"
    curl -L "$URL_2" -o "$MODEL_2"
else
    echo "$MODEL_2 파일이 이미 존재함. 다운로드 셍략"
fi

# 다시 원래 폴더로 복귀
cd ..

# Docker Compose 실행
echo "Docker Compose를 사용하여 API 컨테이너 빌드"
if docker compose version &> /dev/null; then
    docker compose up -d --build
else
    docker-compose up -d --build
fi

# 완료 안내 메시지
echo "Swagger UI에 접속: http://127.0.0.1:8005/docs"

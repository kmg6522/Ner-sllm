FROM python:3.11-slim

# llama-cpp-python 설치에 필요한 C++ 빌드 도구 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    cmake \
    python3-dev \
    ninja-build \
    git \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 나머지 소스코드 복사
COPY . .

# FastAPI 기본 포트
EXPOSE 8005

# 서버 실행 명령어 (외부 접속을 위해 host를 0.0.0.0으로 설정)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8005"]
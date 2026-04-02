# FastAPI 앱 진입점
# 앱 인스턴스 생성과 라우터 등록만 담당합니다.

from fastapi import FastAPI
from app.routers.extract import router as extract_router

app = FastAPI(
    title="NER-SLLM API",
    description="게시글에서 상품명, 브랜드 등 핵심 정보를 JSON 형태로 추출하는 API",
    version="1.0.0",
)

app.include_router(extract_router)
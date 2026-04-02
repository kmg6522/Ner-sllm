# NER 추출 엔드포인트
# /extract, /health API 라우터를 정의

from fastapi import APIRouter, HTTPException
from app.schemas import TextRequest, NERResponse
from app.config import MODEL_PATH
from app.services.llm_service import run_extraction
from app.utils.parser import clean_think_tags, extract_json, build_ner_result

router = APIRouter()


@router.get("/health")
async def health_check():
    return {"status": "ok", "model": MODEL_PATH}


@router.post("/extract", response_model=NERResponse)    # 클라이언트에게 돌려줄 데이터 형태 정의
async def extract(request: TextRequest):    # 클라이언트로부터 받은 데이터 형태 정의
    try:
        raw_text = run_extraction(request.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"모델 추론 중 오류 발생: {str(e)}")

    # 후처리: think 태그 제거 → JSON 추출 → NER 필드 정리
    cleaned_text = clean_think_tags(raw_text)
    parsed = extract_json(cleaned_text, raw_text)
    result = build_ner_result(parsed)

    return NERResponse(**result)
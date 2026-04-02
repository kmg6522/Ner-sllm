import re
import json
from fastapi import HTTPException


def clean_think_tags(text: str) -> str:
    """Qwen3.5의 <think>...</think> 태그를 제거"""
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


def extract_json(text: str, raw_text: str) -> dict:
    """JSON 객체를 추출, 파싱"""
    json_match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not json_match:
        raise HTTPException(
            status_code=422,
            detail=f"모델 응답에서 JSON을 찾을 수 없음. 원본 응답: {raw_text}"
        )

    try:
        return json.loads(json_match.group())
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=422,
            detail=f"모델 응답 JSON 파싱 실패. 원본 응답: {raw_text}"
        )


def build_ner_result(parsed: dict) -> dict:
    """파싱된 딕셔너리에서 NER 필드를 추출하고, 누락 시 '없음' 설정"""
    return {
        "ORG": parsed.get("ORG", "없음"),
        "AF": parsed.get("AF", "없음"),
        "QT": parsed.get("QT", "없음"),
        "CL": parsed.get("CL", "없음"),
        "GN": parsed.get("GN", "없음"),
    }
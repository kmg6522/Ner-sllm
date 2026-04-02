# Pydantic 요청/응답 모델 정의
# API의 입출력 데이터 구조를 정의
from pydantic import BaseModel, Field

class TextRequest(BaseModel):
    text: str = Field(..., description="추출할 중고거래 게시글 텍스트")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "text": "(미개봉) 아디다스 가젤 블랙 270 남성용 7만원에 팝니다."
                }
            ]
        }
    }

class NERResponse(BaseModel):
    ORG: str
    AF: str
    QT: str
    CL: str
    GN: str
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from llama_cpp import Llama
import re
import json

app = FastAPI(
    title="NER-SLLM API", 
    description="게시글에서 상품명, 브랜드 등 핵심 정보를 JSON 형태로 추출하는 API",
    version="1.0.0"
)
# 모델 경로 설정
MODEL_PATH = "/app/models/Qwen3.5-0.8B-Q4_K_M.gguf"
# MODEL_PATH = "/app/models/Qwen3.5-2B-Q4_K_M.gguf"

# 모델 로드
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=1024,      # 컨텍스트 길이
    n_gpu_layers=0, # GPU 레이어 수 (0이면 CPU에서 실행)
    verbose=True    # 불필요한 엔진 로그 숨김
)
print("모델 로딩 완료")

# 요청 및 응답 데이터 구조
class TextRequest(BaseModel):
    text: str = Field(..., description="추출할 중고거래 게시글 텍스트")

    # Swagger UI의 'Request body'에 기본값으로 들어갈 내용
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

@app.get("/health")
async def health_check():
    return {"status": "ok", "model": MODEL_PATH}

@app.post("/extract", response_model=NERResponse)
async def extract(request: TextRequest):
    try:
        system_prompt = """너는 중고거래 게시글에서 정보를 추출하는 전문 AI야.
반드시 다음 순서와 양식에 맞춰서 단 한 줄로만 대답해. 해당 정보가 문장에 없으면 '없음'이라고 적어.
출력 양식:
{
  "ORG": "조직/브랜드",
  "AF": "상품명",
  "QT": "수량/금액",
  "CL": "색상/분류",
  "GN": "성별/일반속성"
}"""

        # 텍스트 전달
        response = llm.create_chat_completion(
            messages=[
                {"role": "system", "content": system_prompt},
                # 예시 1
                {"role": "user", "content": "나이키 에어포스 1 화이트 260 남성용 5만원에 팝니다"},
                {"role": "assistant", "content": '{"ORG": "나이키", "AF": "에어포스 1", "QT": "5만원", "CL": "화이트", "GN": "260, 남성용"}'},
                # 예시 2
                {"role": "user", "content": "아이패드 프로 11인치 미개봉 100만원 급처"},
                {"role": "assistant", "content": '{"ORG": "없음", "AF": "아이패드 프로 11인치", "QT": "100만원", "CL": "없음", "GN": "미개봉"}'},
                # 실제 인풋
                {"role": "user", "content": request.text}
            ],
            max_tokens=200,  
            temperature=0.1 
        )
        
        # 텍스트 결과물 추출
        raw_text = response["choices"][0]["message"]["content"].strip()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"모델 추론 중 오류 발생: {str(e)}")

    # <think>...</think> 태그 제거 (Qwen3.5 thinking 출력 대응)
    cleaned_text = re.sub(r"<think>.*?</think>", "", raw_text, flags=re.DOTALL).strip()

    # JSON 부분 추출
    json_match = re.search(r"\{.*\}", cleaned_text, flags=re.DOTALL)
    if not json_match:
        raise HTTPException(
            status_code=422,
            detail=f"모델 응답에서 JSON을 찾을 수 없음. 원본 응답: {raw_text}"
        )

    try:
        parsed = json.loads(json_match.group())
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=422,
            detail=f"모델 응답 JSON 파싱 실패. 원본 응답: {raw_text}"
        )

    # 필드 누락 시 기본값 '없음' 처리
    result = {
        "ORG": parsed.get("ORG", "없음"),
        "AF": parsed.get("AF", "없음"),
        "QT": parsed.get("QT", "없음"),
        "CL": parsed.get("CL", "없음"),
        "GN": parsed.get("GN", "없음"),
    }

    return NERResponse(**result)
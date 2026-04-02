from llama_cpp import Llama
from app.config import MODEL_PATH, N_CTX, N_GPU_LAYERS, VERBOSE

# 모델을 모듈 레벨에서 한 번만 로드
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=N_CTX,
    n_gpu_layers=N_GPU_LAYERS,
    verbose=VERBOSE,
)

# 시스템 프롬프트 (NER 추출용)
SYSTEM_PROMPT = """너는 중고거래 게시글에서 정보를 추출하는 전문 AI야.
반드시 다음 순서와 양식에 맞춰서 단 한 줄로만 대답해. 해당 정보가 문장에 없으면 '없음'이라고 적어.
출력 양식:
{
  "ORG": "조직/브랜드",
  "AF": "상품명",
  "QT": "수량/금액",
  "CL": "색상/분류",
  "GN": "성별/일반속성"
}"""

# Few-shot 예시 메시지
FEW_SHOT_MESSAGES = [
    {"role": "user", "content": "나이키 에어포스 1 화이트 260 남성용 5만원에 팝니다"},
    {"role": "assistant", "content": '{"ORG": "나이키", "AF": "에어포스 1", "QT": "5만원", "CL": "화이트", "GN": "260, 남성용"}'},
    {"role": "user", "content": "아이패드 프로 11인치 미개봉 100만원 급처"},
    {"role": "assistant", "content": '{"ORG": "없음", "AF": "아이패드 프로 11인치", "QT": "100만원", "CL": "없음", "GN": "미개봉"}'},
]


def run_extraction(user_text: str) -> str:
    """사용자 텍스트를 받아 추론을 수행 및 응답 텍스트를 반환"""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *FEW_SHOT_MESSAGES,
        {"role": "user", "content": user_text},
    ]

    response = llm.create_chat_completion(
        messages=messages,
        max_tokens=200,
        temperature=0.1,
    )

    return response["choices"][0]["message"]["content"].strip()
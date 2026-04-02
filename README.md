# NER-SLLM API

중고거래 게시글에서 **상품명, 브랜드, 금액, 색상, 속성** 등 핵심 정보를 JSON으로 추출하는 경량 NER API입니다.

sLLM(Qwen3.5 GGUF)을 llama-cpp-python으로 로컬 추론하며, FastAPI 기반으로 동작합니다.

## 빠른 시작
docker가 실행중임을 가정하고 진행
```bash
git clone https://github.com/kmg6522/Ner-sllm.git
cd Ner-sllm
bash start_script.sh
```

스크립트가 자동으로:
1. 모델 파일 다운로드 (Hugging Face → `models/`)
2. Docker 이미지 빌드 및 컨테이너 실행

완료 후 **Swagger UI**: http://127.0.0.1:8005/docs

## 프로젝트 구조

```
├── main.py                      # 앱 진입점 (FastAPI 인스턴스 생성 + 라우터 등록)
├── app/
│   ├── __init__.py              # 패키지 선언
│   ├── config.py                # 설정값 관리 (MODEL_PATH, N_CTX 등)
│   ├── schemas.py               # Pydantic 요청/응답 모델 (TextRequest, NERResponse)
│   ├── services/
│   │   ├── __init__.py
│   │   └── llm_service.py       # LLM 모델 로드 + 추론 함수
│   ├── routers/
│   │   ├── __init__.py
│   │   └── extract.py           # /health, /extract 엔드포인트 정의
│   └── utils/
│       ├── __init__.py
│       └── parser.py            # 응답 후처리 (think 태그 제거, JSON 파싱)
├── models/                      # GGUF 모델 파일 저장 디렉토리
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── start_script.sh              # 모델 다운로드 + Docker 빌드/실행 스크립트
```

### 각 모듈 설명

| 파일 | 역할 |
|------|------|
| `main.py` | FastAPI 앱 인스턴스 생성, 라우터 등록만 수행 |
| `app/config.py` | `MODEL_PATH`, `N_CTX`, `N_GPU_LAYERS` 등 전역 설정값 관리 |
| `app/schemas.py` | API 입출력 데이터 구조 정의 (`TextRequest`, `NERResponse`) |
| `app/services/llm_service.py` | Llama 모델 로드(싱글턴) + `run_extraction()` 추론 함수 + 프롬프트/few-shot 관리 |
| `app/routers/extract.py` | `/extract`, `/health` API 엔드포인트를 `APIRouter`로 정의 |
| `app/utils/parser.py` | `clean_think_tags()`, `extract_json()`, `build_ner_result()` 후처리 유틸리티 |

## API 엔드포인트

### `POST /extract`

중고거래 게시글 텍스트에서 개체명을 추출합니다.

**요청:**
```json
{
  "text": "나이키 에어포스 1 화이트 260 남성용 5만원에 팝니다"
}
```

**응답:**
```json
{
  "ORG": "나이키",
  "AF": "에어포스 1",
  "QT": "5만원",
  "CL": "화이트",
  "GN": "260, 남성용"
}
```

| 필드 | 설명 |
|------|------|
| `ORG` | 조직/브랜드 |
| `AF` | 상품명 |
| `QT` | 수량/금액 |
| `CL` | 색상/분류 |
| `GN` | 성별/일반속성 |

### `GET /health`

서버 상태 확인용 헬스체크 엔드포인트입니다.

## 사용 모델

| 모델 | 크기 | 용도 |
|------|------|------|
| `Qwen3.5-0.8B-Q4_K_M.gguf` | ~0.5GB | 기본 (빠른 응답) |
| `Qwen3.5-2B-Q4_K_M.gguf` | ~1.5GB | 고품질 추출 |

기본값은 0.8B 모델입니다. `app/config.py`에서 `MODEL_PATH`를 변경하여 2B 모델로 전환할 수 있습니다.

## 기술 스택

- **FastAPI** - REST API 프레임워크
- **llama-cpp-python** - GGUF 모델 추론 엔진
- **Qwen3.5** - sLLM 모델 (Alibaba)
- **Docker** - 컨테이너 배포
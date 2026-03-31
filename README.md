# NER-SLLM API

중고거래 게시글에서 **상품명, 브랜드, 금액, 색상, 속성** 등 핵심 정보를 JSON으로 추출하는 경량 NER API입니다.

sLLM(Qwen3.5 GGUF)을 llama-cpp-python으로 로컬 추론하며, FastAPI 기반으로 동작합니다.

## 빠른 시작

```bash
git clone https://github.com/kmg6522/Ner-sllm.git
cd Ner-sllm
bash start_script.sh
```

스크립트가 자동으로:
1. 모델 파일 다운로드 (Hugging Face → `models/`)
2. Docker 이미지 빌드 및 컨테이너 실행

완료 후 **Swagger UI**: http://127.0.0.1:8000/docs

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

기본값은 0.8B 모델입니다. `main.py`에서 `MODEL_PATH`를 변경하여 2B 모델로 전환할 수 있습니다.

## 기술 스택

- **FastAPI** - REST API 프레임워크
- **llama-cpp-python** - GGUF 모델 추론 엔진
- **Qwen3.5** - sLLM 모델 (Alibaba)
- **Docker** - 컨테이너 배포
# 🧩 코드 컨벤션: Python 네이밍 규칙

본 프로젝트는 Python 기반이며, 코드의 일관성과 가독성을 유지하기 위해 다음과 같은 네이밍 규칙을 따릅니다. 이 규칙은 [PEP8](https://peps.python.org/pep-0008/) 및 실무 기준을 반영합니다.

---

## 📁 1. 파일 및 디렉토리

| 항목 | 규칙 | 예시 |
|------|------|------|
| 파일 이름 | 소문자 + 언더스코어 (`snake_case`) | `user_service.py`, `data_loader.py` |
| 디렉토리 이름 | 소문자, 필요 시 `_` 사용 가능 | `utils/`, `models/`, `api/` |

---

## 🧱 2. 클래스 및 예외 클래스

| 항목 | 규칙 | 예시 |
|------|------|------|
| 클래스 이름 | 파스칼 케이스 (`PascalCase`) | `User`, `BaseModel`, `DataLoader` |
| 예외 클래스 | 파스칼 케이스 + `Error` / `Exception` 접미어 | `ValidationError`, `APIException` |

---

## 🧪 3. 함수 및 변수

| 항목 | 규칙 | 예시 |
|------|------|------|
| 함수 이름 | 스네이크 케이스 (`snake_case`) | `get_user_info()`, `load_data()` |
| 변수 이름 | 스네이크 케이스 | `user_name`, `max_count` |
| 상수 이름 | 모두 대문자 + 언더스코어 | `MAX_RETRIES`, `DEFAULT_TIMEOUT` |

---

## ✅ 4. 타입 힌트 (Python 3.9+ 기준)

```python
def get_user_name(user_id: int) -> str:
    ...

class User:
    name: str
    age: int

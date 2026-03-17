# 수정 사항 정리

## 발견된 문제 및 해결 방법

### 1. ❌ pushover-python 버전 오류

**문제**:
- requirements.txt에서 `pushover-python==0.1.1` 지정
- PyPI에는 0.1.1 버전이 없고 0.1.2만 존재

**해결**:
```diff
- pushover-python==0.1.1
+ pushover-python==0.1.2
```

---

### 2. ❌ Pushover API 호환성 문제

**문제**:
- 코드에서 `from pushover import Client` 사용
- 실제 라이브러리에는 `Pushover` 클래스만 존재
- `Client` 클래스는 존재하지 않음

**해결**:
```python
# 변경 전
from pushover import Client
self.client = Client(user_key, api_token=api_token)
self.client.send_message(...)

# 변경 후
from pushover import Pushover
self.client = Pushover(token=api_token, user=user_key)
self.client.notify(message=message, title=title, url=link, url_title="게시글 보기")
```

---

### 3. ❌ BoardMonitor 생성자 불일치

**문제**:
- main.py에서 `BoardMonitor(config_path=CONFIG_FILE)` 호출
- monitor.py의 `__init__`에서 이 매개변수 미수신

**해결**:
```python
# 변경 전
def __init__(self):
    self.config_manager = ConfigManager()

# 변경 후
def __init__(self, config_path: str = 'config.ini'):
    self.config_manager = ConfigManager(config_path)
```

---

### 4. ❌ 필수 설정값 검증 오류

**문제**:
- Pushover USER_KEY와 API_TOKEN이 없으면 애플리케이션 시작 불가
- 테스트 실행이 어려움

**해결**:
- 환경변수 지원 추가 (`BOARD_MONITOR_PUSHOVER_USER_KEY`, `BOARD_MONITOR_PUSHOVER_API_TOKEN`)
- 환경변수가 있으면 config.ini의 플레이스홀더 값 무시

```python
# config.py get() 메서드 개선
def get(self, section: str, key: str, default: Optional[str] = None) -> str:
    # 1. 환경변수 확인
    env_var = f"BOARD_MONITOR_{section}_{key}".upper()
    env_value = os.getenv(env_var)
    if env_value:
        return env_value
    
    # 2. config.ini 파일 확인
    return self.config.get(section, key)
```

---

## 설정 방법

### 방법 1: config.ini 직접 편집 (추천)

```ini
[PUSHOVER]
USER_KEY = your_pushover_user_key
API_TOKEN = your_pushover_api_token
```

### 방법 2: 환경변수 사용

```bash
# Windows (PowerShell)
$env:BOARD_MONITOR_PUSHOVER_USER_KEY = "your_pushover_user_key"
$env:BOARD_MONITOR_PUSHOVER_API_TOKEN = "your_pushover_api_token"
python main.py

# Linux/Mac (Bash)
export BOARD_MONITOR_PUSHOVER_USER_KEY="your_pushover_user_key"
export BOARD_MONITOR_PUSHOVER_API_TOKEN="your_pushover_api_token"
python main.py

# Docker
docker run -e BOARD_MONITOR_PUSHOVER_USER_KEY="..." \
           -e BOARD_MONITOR_PUSHOVER_API_TOKEN="..." \
           board-monitor
```

---

## 수정된 파일 목록

| 파일 | 수정 사항 |
|------|---------|
| `requirements.txt` | pushover-python 버전 0.1.1 → 0.1.2 |
| `src/notifier.py` | Pushover API 호환성 수정 |
| `src/monitor.py` | BoardMonitor 생성자에 config_path 매개변수 추가 |
| `src/config.py` | 환경변수 지원 추가 |

---

## 테스트 결과

```
✅ 모든 Python 파일 컴파일 성공
✅ BoardMonitor 생성 성공
✅ 설정 검증 완료
✅ 환경변수 오버라이드 지원 확인
```

---

## 실행 방법

```bash
# 1. 의존성 설치
pip install -r requirements.txt

# 2. config.ini 설정 또는 환경변수 설정
# - config.ini 편집하거나
# - 환경변수 BOARD_MONITOR_PUSHOVER_USER_KEY, BOARD_MONITOR_PUSHOVER_API_TOKEN 설정

# 3. 애플리케이션 실행
python main.py
```

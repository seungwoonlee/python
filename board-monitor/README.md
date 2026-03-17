# Board Monitor - 게시판 모니터링 애플리케이션

Python 기반 게시판 모니터링 애플리케이션입니다. DC인사이드 게시판을 주기적으로 감시하여 특정 키워드가 포함된 새 글이 올라오면 Pushover 서비스를 통해 알림을 전송합니다.

## 기능

- **자동 게시판 모니터링**: 설정된 주기로 게시판을 감시
- **키워드 필터링**: 여러 개의 키워드로 게시글 필터링
- **Pushover 알림**: 조건을 만족하는 게시글에 대해 실시간 알림 전송
- **중복 방지**: 이미 알림을 보낸 게시글 추적 및 관리
- **메모리 효율**: 최대 500개의 ID만 메모리에 유지
- **로깅**: 상세한 로그 기록 및 디버깅 정보

## 프로젝트 구조

```
board-monitor/
├── main.py                 # 애플리케이션 엔트리 포인트
├── config.ini             # 설정 파일
├── requirements.txt       # Python 의존성
├── Dockerfile            # Docker 컨테이너화
├── .gitignore           # Git 무시 파일
└── src/
    ├── __init__.py       # 패키지 초기화
    ├── config.py         # 설정 관리
    ├── logger.py         # 로깅 설정
    ├── scraper.py        # 웹 페이지 수집
    ├── parser.py         # HTML 파싱
    ├── filter.py         # 필터 및 중복 관리
    ├── notifier.py       # Pushover 알림
    └── monitor.py        # 메인 모니터링 로직
```

## 설치 및 사용

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 설정

`config.ini` 파일을 수정하여 다음을 설정하세요:

- **Pushover 인증정보**: USER_KEY, API_TOKEN
- **감시할 키워드**: KEYWORDS
- **체크 간격**: CHECK_INTERVAL_SECONDS
- **게시판 URL 및 CSS Selector**: TARGET 섹션

### 3. 실행

```bash
python main.py
```

### 4. Docker로 실행

```bash
docker build -t board-monitor .
docker run -d --name board-monitor board-monitor
```

## 설정 파일 (config.ini)

### [TARGET]
- `URL`: 감시할 게시판 URL
- `POST_SELECTOR`: 게시글을 감싸는 HTML 요소의 CSS Selector
- `TITLE_SELECTOR`: 제목 요소의 CSS Selector
- `LINK_SELECTOR`: 링크 요소의 CSS Selector
- `ID_SELECTOR`: 게시글 ID 요소의 CSS Selector

### [FILTER]
- `KEYWORDS`: 감시할 키워드 목록 (쉼표로 구분)

### [PUSHOVER]
- `USER_KEY`: Pushover 사용자 키 (https://pushover.net 에서 발급)
- `API_TOKEN`: Pushover 애플리케이션 API 토큰

### [APP]
- `CHECK_INTERVAL_SECONDS`: 모니터링 주기 (초)
- `MAX_TRACKED_IDS`: 추적할 최대 ID 개수
- `REQUEST_TIMEOUT`: HTTP 요청 타임아웃 (초)
- `LOG_LEVEL`: 로그 레벨 (DEBUG, INFO, WARNING, ERROR, CRITICAL)

## 모듈 설명

### config.py
설정 파일 관리 및 검증 담당

### logger.py
구조화된 로깅 설정 (콘솔 및 파일 출력)

### scraper.py
HTTP 요청을 통한 웹 페이지 수집

### parser.py
BeautifulSoup을 사용한 HTML 파싱 및 게시글 추출

### filter.py
키워드 필터링 및 중복 게시글 추적

### notifier.py
Pushover를 통한 알림 전송

### monitor.py
전체 모니터링 워크플로우 조율

## 주요 개선사항

- ✅ **모듈식 구조**: 단일 파일에서 기능별 모듈로 분리
- ✅ **향상된 에러 처리**: 상세한 예외 처리 및 로깅
- ✅ **Graceful Shutdown**: SIGINT/SIGTERM 신호 처리
- ✅ **로그 파일 지원**: 콘솔 및 파일 동시 로깅
- ✅ **환경 설정 지원**: 기본값 제공 및 환경변수 오버라이드
- ✅ **타임존 설정**: Docker 컨테이너에서 한국 시간대 적용
- ✅ **메모리 최적화**: 추적 ID 자동 정리
- ✅ **상세한 로깅**: 각 단계별 디버깅 정보 제공

## 라이선스

MIT License

"""
보드 모니터 - 아키텍처 및 설계 문서
"""

# Board Monitor Architecture

## 개요

Board Monitor는 게시판 모니터링을 위한 모듈식 애플리케이션으로, 단일 책임 원칙(SRP)을 따르는 각 모듈로 구성되어 있습니다.

## 시스템 아키텍처

```
┌─────────────────────────────────────────────────────────┐
│                    BoardMonitor                         │
│                  (메인 조율자)                           │
└──────────┬────────────────────────────────────┬─────────┘
           │                                    │
    ┌──────▼──────┐                    ┌───────▼────────┐
    │  ConfigMgr  │                    │    Logger      │
    │ 설정 관리    │                    │  로깅 관리     │
    └─────────────┘                    └────────────────┘
           │
    ┌──────▼──────────────────────────────────┐
    │         Scraper                         │
    │      웹 페이지 수집                      │
    └──────┬───────────────────────────────────┘
           │
           │ HTML
    ┌──────▼──────────────────────────────────┐
    │         Parser                          │
    │   게시글 정보 추출                       │
    └──────┬────────────────────────┬──────────┘
           │ List[Post]             │
           │                        │
    ┌──────▼──────────────────┐    │
    │       Filter            │    │
    │ 키워드 필터링/중복제거   │◄───┘
    └──────┬───────────────────┘
           │ 새 게시글
    ┌──────▼────────────────────────┐
    │     NotificationManager       │
    │     Pushover 알림 전송         │
    └───────────────────────────────┘
```

## 모듈 상세 설명

### 1. ConfigManager (config.py)
- **책임**: 설정 파일(config.ini) 로드 및 검증
- **주요 기능**:
  - 설정값 조회 (문자열, 정수)
  - 필수값 검증
  - 기본값 제공
  - 설정 파일 자동 생성

- **API**:
  ```python
  config = ConfigManager('config.ini')
  config.validate()  # 필수값 검증
  url = config.get('TARGET', 'URL')
  timeout = config.get_int('APP', 'REQUEST_TIMEOUT', 10)
  ```

### 2. Logger (logger.py)
- **책임**: 구조화된 로깅 설정
- **주요 기능**:
  - 콘솔 및 파일 동시 로깅
  - 로그 레벨 설정
  - 타임스탬프 포함
  - 싱글톤 패턴

- **API**:
  ```python
  logger = Logger.setup(level='INFO', log_file='app.log')
  logger.info("정보 메시지")
  logger.error("오류 메시지")
  ```

### 3. Scraper (scraper.py)
- **책임**: 웹 페이지 수집
- **주요 기능**:
  - HTTP GET 요청
  - 타임아웃 관리
  - User-Agent 설정
  - 상세한 오류 처리

- **API**:
  ```python
  scraper = Scraper(timeout=10)
  html = scraper.fetch('https://example.com')
  ```

### 4. Parser (parser.py)
- **책임**: HTML 파싱 및 게시글 추출
- **주요 기능**:
  - CSS Selector 기반 파싱
  - Post 객체 생성
  - 상대 경로 → 절대 경로 변환
  - 유효성 검증 (숫자 ID만 선택)

- **API**:
  ```python
  parser = Parser(base_url='https://example.com')
  posts = parser.parse_posts(html, '.post', '.title a', '.link', '.id')
  # returns List[Post]
  ```

### 5. Filter (filter.py)
- **책임**: 키워드 필터링 및 중복 제거
- **주요 기능**:
  - 키워드 매칭 (대소문자 무시)
  - 알림 전송 이력 추적
  - 메모리 효율 (최대 500개 ID 유지)
  - 첫 실행 초기화

- **API**:
  ```python
  filter = Filter(keywords=['키워드1', '키워드2'], max_tracked_ids=500)
  if filter.is_keyword_match(text):
      filter.add_notified_id(post_id)
  ```

### 6. NotificationManager (notifier.py)
- **책임**: Pushover를 통한 알림 전송
- **주요 기능**:
  - Pushover 클라이언트 관리
  - 알림 메시지 구성
  - URL 링크 포함
  - 오류 처리

- **API**:
  ```python
  notifier = NotificationManager(user_key, api_token)
  notifier.send(post_id, title, link, keyword)
  ```

### 7. BoardMonitor (monitor.py)
- **책임**: 전체 모니터링 워크플로우 조율
- **주요 기능**:
  - 초기화 및 설정 관리
  - 메인 모니터링 루프
  - Graceful shutdown 처리
  - 신호 핸들러 등록

- **API**:
  ```python
  monitor = BoardMonitor()
  monitor.run()  # 메인 루프 시작
  ```

## 데이터 흐름

```
┌─────────────────────────────────┐
│   1. 설정 로드 (ConfigManager)  │
└──────────────┬──────────────────┘
               │
┌──────────────▼──────────────────┐
│  2. 웹 페이지 수집 (Scraper)    │
│  HTTP GET 요청                  │
└──────────────┬──────────────────┘
               │ HTML
┌──────────────▼──────────────────┐
│  3. 게시글 파싱 (Parser)        │
│  CSS Selector로 정보 추출       │
└──────────────┬──────────────────┘
               │ Post[]
┌──────────────▼──────────────────┐
│  4. 필터링 (Filter)             │
│  - 첫 실행: 초기화              │
│  - 이후: 새 글만 선택           │
│  - 키워드 매칭 확인             │
│  - 중복 제거                    │
└──────────────┬──────────────────┘
               │ 새 게시글
┌──────────────▼──────────────────┐
│  5. 알림 전송 (Notifier)        │
│  Pushover로 알림 전송           │
└──────────────┬──────────────────┘
               │
┌──────────────▼──────────────────┐
│  6. 대기 (Sleep)                │
│  설정된 간격만큼 대기            │
└──────────────┬──────────────────┘
               │
               └───► 3단계로 돌아감
```

## 클래스 다이어그램

```
Config Manager
├── load_config(): None
├── get(section, key, default): str
├── get_int(section, key, default): int
├── validate(): None
└── save_default_config(): None

Logger
├── setup(level, log_file): Logger
└── get_logger(): Logger

Scraper
├── fetch(url): Optional[str]
└── _handle_errors(): None

Parser
├── parse_posts(...): List[Post]
└── _extract_post(...): Optional[Post]

Post
├── __init__(id, title, link)
├── to_dict(): Dict
└── __repr__(): str

Filter
├── is_keyword_match(text): bool
├── add_notified_id(id): None
├── is_already_notified(id): bool
├── initialize_with_ids(ids): None
└── _cleanup_old_ids(): None

NotificationManager
├── __init__(user_key, api_token)
└── send(id, title, link, keyword): bool

BoardMonitor
├── setup(): bool
├── run(): None
├── _monitor_once(): None
├── _signal_handler(signum, frame): None
└── _cleanup(): None
```

## 디자인 패턴

### 1. 싱글톤 패턴
- **Logger**: 애플리케이션 전역에서 단일 인스턴스 사용

### 2. 정책 패턴
- **Filter**: 키워드 필터링 로직의 추상화

### 3. 팩토리 패턴
- **ConfigManager**: 설정 생성 및 관리

### 4. 옵저버 패턴
- **신호 핸들러**: SIGINT/SIGTERM 이벤트 처리

## 오류 처리 전략

### 계층별 오류 처리

```
┌─────────────────────────────────┐
│   BoardMonitor.run()            │
│   전체 루프 예외 처리             │
└────────────────┬────────────────┘
                 │
        ┌────────▼─────────┐
        │ _monitor_once()  │
        │ 각 사이클 예외 처리│
        └────────┬─────────┘
                 │
    ┌────────────┼────────────┐
    │            │            │
┌───▼──┐   ┌────▼───┐  ┌────▼────┐
│Parser│   │Scraper │  │ Filter  │
│예외  │   │예외    │  │예외    │
└──────┘   └────────┘  └────────┘
```

## 성능 특성

| 작업 | 복잡도 | 설명 |
|------|--------|------|
| 게시글 파싱 | O(n) | n = 게시글 수 |
| 키워드 매칭 | O(k*m) | k = 키워드 수, m = 평균 제목 길이 |
| 중복 확인 | O(1) | Set 기반 조회 |
| ID 정리 | O(n log n) | n = 추적 ID 수 (최대 500) |
| 메모리 사용 | O(n) | n = 추적 ID 수 |

## 확장 포인트

### 1. 다른 알림 서비스 추가
```python
class SlackNotifier(NotificationManager):
    """Slack 알림 지원"""
    pass

class EmailNotifier(NotificationManager):
    """이메일 알림 지원"""
    pass
```

### 2. 다른 게시판 지원
```python
class NaverCafeParser(Parser):
    """네이버 카페 파싱"""
    pass

class BlogParser(Parser):
    """블로그 파싱"""
    pass
```

### 3. 데이터베이스 지원
```python
class DatabaseFilter(Filter):
    """DB 기반 중복 관리"""
    pass
```

## 의존성 관리

```
main.py
  └─ monitor.py (BoardMonitor)
      ├─ config.py (ConfigManager)
      ├─ logger.py (Logger)
      ├─ scraper.py (Scraper)
      │   └─ requests
      ├─ parser.py (Parser)
      │   └─ bs4 (BeautifulSoup)
      ├─ filter.py (Filter)
      └─ notifier.py (NotificationManager)
          └─ pushover
```

## 배포 고려사항

### 로컬 실행
```bash
python main.py
```

### Docker 실행
```bash
docker build -t board-monitor .
docker run -d \
  -v $(pwd)/config.ini:/app/config.ini \
  -v $(pwd)/logs:/app/logs \
  board-monitor
```

### 로그 모니터링
```bash
# 실시간 로그 확인
tail -f board_monitor.log

# 에러 로그만 확인
grep ERROR board_monitor.log
```

## 보안 고려사항

1. **설정 파일 보안**
   - Pushover 키를 환경변수로 관리
   - .gitignore에 config.ini 추가

2. **User-Agent 설정**
   - 모든 HTTP 요청에 User-Agent 헤더 포함
   - 봇 차단 우회

3. **타임아웃 설정**
   - HTTP 요청에 타임아웃 적용 (기본값 10초)
   - 무한 대기 방지

4. **로그 민감정보**
   - 민감한 정보는 로깅하지 않음
   - DEBUG 레벨에서만 상세 정보 출력

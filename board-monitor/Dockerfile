# 1. 베이스 이미지 선택 (Python 3.11 슬림 버전)
FROM python:3.11-slim

# 2. 타임존 설정 (한국 시간대)
ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 3. 작업 디렉토리 설정
WORKDIR /app

# 4. 필요한 파일 복사
# requirements.txt를 먼저 복사하여 라이브러리 설치를 캐싱
COPY requirements.txt .

# 5. 파이썬 라이브러리 설치
RUN pip install --no-cache-dir -r requirements.txt

# 6. 나머지 소스 코드 복사
COPY . .

# 7. 컨테이너 실행 시 실행될 명령어
CMD ["python", "main.py"]

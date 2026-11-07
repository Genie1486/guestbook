# 베이스 이미지 선택
FROM python:3.11-slim

# 환경변수 설정
ENV FLASK_APP=app.py    
ENV APP_HOME=/app

# 시스템 패키지 설치 (vi 편집기)
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR ${APP_HOME}

# 앱 코드 복사
COPY requirements.txt .
COPY . .

# Python 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 포트 노출
EXPOSE 5000

# 헬스체크
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# 서버 실행
CMD ["python", "app.py"]
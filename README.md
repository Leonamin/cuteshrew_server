# 귀여운 땃쥐 서버

## 환경 설정
project 폴더 아래에 .env를 생성하고 config.py에서 필요한 필드를 작성한다 (ex - PROJECT_NAME, VERSION)
- ENVIRONMENT: local로 적지 않으면 openapi_url = None로 하기 때문에 /docs, /redoc은 안보이게 될 것이다.


### .env
```
PROJECT_NAME=cuteshrew
VERSION=1
ENVIRONMENT=local
SHOW_DOCS_ENVIRONMENT=local
SECRET_KEY= openssl rand -hex 32 명령어의 결과물
DATEBASE_PATH=sqlite:///var/db/cuteshrew.db
```

## 실행
### 테스트
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

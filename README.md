# 귀여운 땃쥐 서버

## 환경 설정
project 폴더 아래에 .env를 생성하고 config.py에서 필요한 필드를 작성한다 (ex - PROJECT_NAME, VERSION)
- SHOW_DOCS: false로 하면 API 스웨거 문서를 숨긴다


### .env
```
PROJECT_NAME=cuteshrew
VERSION=0.1.0
ENVIRONMENT=local
SHOW_DOCS=True
SECRET_KEY=asdaj543lkj12iu2982739179hjkadshlk
DATABASE_URL=sqlite:///./db.sqlite3
```

- PROJECT_NAME: 프로젝트 이름 [project name]
- VERSION: 버전 코드 [1.0.0]
- ENVIRONMENT: 환경 설정 [local]
- SHOW_DOCS: [True | False]
- SECRET_KEY= openssl rand -hex 32 결과물
- DATABASE_URL= DB URL


## 실행
### 테스트
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

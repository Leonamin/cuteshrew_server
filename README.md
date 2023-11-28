# Cute Shrew
이것 땃쥐에요!

## 파이썬 실행환경
1. python -m venv .venv
2. .\venv\Sripts\Activate.ps1 (Windows), source .venv/bin/activate(Ubuntu)
3. (venv 환경에서) pip install -r requirements.txt

## 서버 실행에 필요
1. 프로젝트 폴더에 `.env`를 생성하고 아래 내용을 작성한다
```
PROJECT_NAME="Cute Shrew"
VERSION="0.0.1"
ENVIRONMENT="dev"

SECRET_KEY="9208d723af982730bce5fe8a8cfafd516d7637ab6daf2c8f526563cb55a09cee"

DB_NAME="cute"
DB_HOST="192.168.0.1"
DB_PORT="3306"
DB_USER="cuteshrew"
DB_PASSWORD="12345678"
DB_CHARSET="utf8mb3"
```
- **ENVIRONMENT**: 서버 환경, 아직 dev, test, prod에 따라 다른 설정은 없고 스웨거 활성화 여부만 달라진다.
- **SECRET_KEY**: JWT 토큰 만들 때 사용할 키 우분투 환경에서는 `openssl rand -hex 32`를 사용하면 아주쉽게! 만들수 있어염
- **DB_xxx**: 말 그대로 DB 설정 현재는 mysql기준임
## 서버 실행
uvicorn app.main:app --host 0.0.0.0 --port 8000

## 번외
- 라이브러리가 추가되거나 변경사항이 생긴다면 **requirements.txt**를 업데이트 해주자(`pip freeze > file_name` 나는 `pip freeze > requirements.txt`)
- DB는 별도 연결 없이 SQLite를 사용중 main파일을 실행하면 `model.Base.metadata.create_all(bind=engine)` 코드가 실행되서 cutehamster.db 파일이 생긴다
- 리눅스에서는 따로 시스템 파일 만들어주자.
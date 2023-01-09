# 귀여운 땃쥐 서버

## 환경 설정
project 폴더 아래에 .env를 생성하고 config.py에서 필요한 필드를 작성한다 (ex - PROJECT_NAME, VERSION)
- ENVIRONMENT: local로 적지 않으면 openapi_url = None로 하기 때문에 /docs, /redoc은 안보이게 될 것이다.

## 실행
### 테스트
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

## 버전 내역
### 0.1
- 버전 명명 시작
### 0.2
- 커뮤니티 정보에 해당 커뮤니티의 전체 게시글 수 추가
- 유저 정보 가져오기 추가
#### 2023-01-04 핫픽스
search에서 게시글, 댓글 불러오기시 커뮤니티, 게시글이 없는 경우에 대한 예외처리 추가
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
### 1.0.0
- 구조 변경
    - Authentication
        - post /signin - 로그인
        - post /verity - AuthToken 타입 토큰 정보 검증
    - user
        - post /user/general - 일반 유저 생성
        - post /user/admin - 비활성
        - get /user/search - 유저 정보 검색
    - comment
        - get /comment/{comment_id} - 댓글 id로 댓글 1개 가져오기
        - get /comment/list/{posting_id} - posting_id로 가져올 만큼 댓글 가져오기
        - get /comment/page/{posting_id}/comment/{page_num} - 페이지 단위로 댓글 가져오기
        - put /comment/{comment_id} - 비활성화
        - delete /comment/{comment_id} - 댓글 id로 댓글 삭제 로그인 필요
        - post /comment/create/{posting_id} - posting_id의 게시글에 댓글 생성 로그인 필요
        - post /comment/reply/create/{group_id} - 비활성화
    - community
        - get /community/all - 이름 잘못 지음 커뮤니티 가져올만큼 가져오기
        - get /community/info - 해당 커뮤니티 정보 가져오기
        - post /community - 커뮤니티 생성하기 로그인 필요 어드민 권한만 가능
        - delete /community - 커뮤니티 삭제하기 로그인 필요 어드민 권한만 가능
    - page - 기존 메인페이지, 커뮤니티 페이지 가져오는 API
        - get /community - 메인 페이지 가져오기
        - get /community/{community_name}/page/{page_num} - 해당 커뮤니티 페이지 가져오기
    - posting - community_name 잘 안써서 경로상 비활성화
        - get /posting/details - 해당 커뮤니티의 자세한 정보를 가진 게시글들 가져오기
        - get /posting/previews - 해당 커뮤니티의 미리보기 정보를 가진 게시글들 가져오기
        - get /posting/{posting_id} - 해당 아이디의 게시글 가져오기
        - put /posting/{posting_id} - 게시글 업데이트하기 커뮤니티도 바꿀수 있다.
        - delete /posting/{posting_id} - 해당 게시글 삭제하기
        - post /posting - 게시글 생성하기
    - search 
        - get /search/posting - 유저 이름으로 검색해서 게시글 가져오기
        - get /searcg/comment - 유저 이름으로 검색해서 댓글 가져오기

#### 2023-01-04 핫픽스
search에서 게시글, 댓글 불러오기시 커뮤니티, 게시글이 없는 경우에 대한 예외처리 추가
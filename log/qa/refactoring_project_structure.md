# 프로젝트 구조 리팩토링 기능 정리
- Community Module
- Posting Module
- Page Module
    - 커뮤니티에서 커뮤니티 정보와 게시글을, 게시글에서 게시글과 커뮤니티 정보를 가져오면 순환 참조가 되기 때문에 페이지라는 라우터를 따로 분리해서 커뮤니티, 게시글의 기능을 이용하고 둘의 데이터를 합쳐서 제공하는 모듈을 만들었다.
# QA
## app.posting.router
### 가져오기
- 올바른 커뮤니티 이름과 올바른 아이디로 가져오기 테스트 완료
    - 비밀번호 걸린 게시물에 비밀번호 테스트 완료
        - 비밀번호 없음
        - 비밀번호 있음 하지만 틀림
        - 비밀번호 있음 맞음
- 올바른 커뮤니티 이름과 올바르지 않은 아이디로 가져오기 테스트 완료
- 올바르지 않은 커뮤니티 이름과 올바른 아이디로 가져오기 테스트 완료
### 리스트 가져오기
- 올바른 커뮤니티 이름으로 가져오기 테스트 완료
    - 최대 개수 만큼 가져오는 것 확인
- 올바르지 않은 커뮤니티 이름으로 가져오기 테스트 완료
    - CommunityNotFound() 응답 확인
- 올바른 커뮤니티 이름과 올바른 개수로 가져오기 테스트 완료
    - 지정한 개수로 가져오는 것 확인
- 올바른 커뮤니티 이름과 101, -1 개로 가져오기 테스트 완료
    - 개수 초과 에러 확인
### 삭제
- 일반 유저 본인 게시글 삭제 테스트 완료
    - 본인 게시글 삭제 가능
- 일반 유저 다른 게시글 삭제 테스트 완료
    - 권한 부족으로 삭제 불가
- 어드민 유저 다른 게시글 삭제 테스트 완료
    - 어드민 권한으로 삭제 가능
- 서브어드민 테스트 아직 안함
### 업데이트
- 일반 유저 본인 게시글 업데이트 테스트 완료
    - 제목 수정
    - 내용 수정
    - 수정 시간 업데이트
    - 비밀번호, 잠김 업데이트
    - 커뮤니티 옮기기 수정
- 일반 유저 다른 게시글 업데이트 테스트 완료
    - Unauthorized 예외 응답
- 어드민 유저 다른 게시글 업데이트 테스트 완료
    - Unauthorized 예외 응답
## app.community.router
### 가져오기
- 커뮤니티 정보 가져오기
    - 커뮤니티가 가진 게시글 개수가 응답에 포함
- 커뮤니티 정보 리스트 가져오기
    - 커뮤니티가 가진 게시글 개수가 응답에 포함
- 커뮤니티 메인페이지 정보 가져오기
    - 커뮤니티에 소속된 게시글을 최신 순으로 가져와서 응답
- 커뮤니티 페이지 정보 가져오기
    - 커뮤니티에 소속된 게시글을 페이지 순서와 개수에 맞게 응답
    - 올바르지 않은 커뮤니티 이름 CommunityNotFound() 응답 확인
    - page_num 0 이하일 경우 InvalidPageNum() 응답 확인
    - 전체 게시글을 초과하는 페이지 숫자에 대해 ExceededPageNum() 응답 확인
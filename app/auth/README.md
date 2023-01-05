# Authentication module
[FastAPI를 시작할 때 모범 사례 및 관례에 대한 의견](https://github.com/zhanymkanov/fastapi-best-practices)에서 안내한 방법을 차근차근 적용하기 위해 준비

auth 폴더 하나가 개별적인 모듈로 동작할 수 있게 한다.

## 1. 프로젝트 구조 일관성있고 예측 가능하게 만들자
1. 모든 도메인 리덱토리틀은 src 폴더 아래에 저장한다.(나 같은 경우는 app 아래다)
- src(app)/ - 어플리케이션의 가장 높은 위치이미 일반적인 모델이나 설정, 상수들을 포함한다.
- src(app)/main.py - FastAPI가 시작하는 프로젝트의 루트
2. 파일별 설명
- router.py - 모든 엔드포인트가 담긴 각 모듈의 코어
- schmas.py - pydantic 모델
- models.py - db 모델
- service.py - 모듈의 상세한 비즈니스 로직
- dependencies.py - 라우터가 의존할 것들
- constants.py - 모듈의 상수 및 에러 코드
- configs.py - 환경 변수
- utils.py - 비즈니스 로직이 아닌 함수들 예: 응답 일반화, 데이터 퓨전(데이터 매핑한다는 의미)
- exceptions.py - 모듈의 상세한 예외들 예 PostNotFound, InvalidUserData
3. 다른 패키지에서 서비스나 디펜던시 상수가 필요하면 - 명시적인 모듈 이름으로 가져온다.
```
from src.auth import constants as auth_constants
from src.notifications import service as notification_service
from src.posts.constants import ErrorCode as PostsErrorCode
```

## 2. 데이터 검증을 하기 위해 Pydantic을 최대한 많이 사용하자
## 3. 데이터 검증에 디펜던시 사용 vs DB
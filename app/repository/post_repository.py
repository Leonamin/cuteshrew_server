from uuid import UUID
from sqlalchemy.orm import Session
from typing import Optional, Tuple

from app.models.post import Post
from app.models.user import User
from app.models.user_profile import UserProfile


class PostRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def find_user_by_id(self, user_id: int) -> Optional[User]:
        """사용자 ID로 사용자 조회"""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def create_draft(self, user_id: int) -> Post:
        """임시저장 게시글 생성"""
        new_draft = Post(
            user_id=user_id,
            title="",
            content="",
            is_draft=True,
        )
        self.db.add(new_draft)
        self.db.commit()
        self.db.refresh(new_draft)
        return new_draft
    
    def find_post_by_id(self, post_id: str) -> Optional[Post]:
        """게시글 ID로 게시글 조회"""
        return self.db.query(Post).filter(Post.id == UUID(post_id)).first()
    
    def update_post(self, post: Post, update_data: dict) -> Post:
        """게시글 업데이트"""
        for field, value in update_data.items():
            if value is not None:
                setattr(post, field, value)
        self.db.commit()
        self.db.refresh(post)
        return post
    
    def get_post_with_writer_info(self, post_id: str) -> Optional[Tuple[Post, str, str]]:
        """게시글과 작성자 정보 함께 조회"""
        db_post = self.find_post_by_id(post_id)
        if not db_post:
            return None
        
        db_user = self.find_user_by_id(db_post.user_id)
        db_user_profile = self.db.query(UserProfile).filter(
            UserProfile.user_id == db_post.user_id
        ).first()
        
        user_name = db_user.name if db_user else ''
        user_thumbnail_url = db_user_profile.thumbnail_url if db_user_profile else ''
        
        return db_post, user_name, user_thumbnail_url

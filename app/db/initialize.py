from sqlalchemy import Engine
from app.db.models import comment, community, post, user

def create_db_metadata(engine: Engine):
    community.Base.metadata.create_all(bind=engine)
    post.Base.metadata.create_all(bind=engine)
    comment.Base.metadata.create_all(bind=engine)
    user.Base.metadata.create_all(bind=engine)
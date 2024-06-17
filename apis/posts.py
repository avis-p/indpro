from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Post, Comment
from schemas import PostCreate, CommentCreate, Post as PostSchema, Comment as CommentSchema

router = APIRouter(tags=["posts"])

@router.post("/posts", response_model=PostSchema)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    db_post = Post(title=post.title, content=post.content, author_id=post.author_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@router.post("/posts/{id}/comments", response_model=CommentSchema)
def add_comment_to_post(id: int, comment: CommentCreate, db: Session = Depends(get_db)):
    db_post = db.query(Post).filter(Post.id == id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db_comment = Comment(post_id=id, author_id=comment.author_id, content=comment.content)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.get("/posts/{id}/comments", response_model=dict)
def get_comments_for_post(id: int, db: Session = Depends(get_db)):
    db_post = db.query(Post).filter(Post.id == id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    comment = db.query(Comment).filter(Comment.post_id == id).all()
    comments = list(map(lambda x: x.to_dict(), comment))
    return {"post_id": id, "comments": comments}
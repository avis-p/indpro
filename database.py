from models import SessionLocal, engine, init_db

init_db()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

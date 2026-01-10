from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

HOST = "localhost"
PORT = 5432
NAME = "ai_assistant_db"
USER = "user"
PASSWORD = "password"

DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}"

engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()

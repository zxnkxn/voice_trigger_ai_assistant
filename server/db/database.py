from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config.config_loader import load_config

# Load database configuration
db_config = load_config("config/database_config.yml")

HOST = db_config["HOST"]
PORT = db_config["PORT"]
NAME = db_config["NAME"]
USER = db_config["USER"]
PASSWORD = db_config["PASSWORD"]

DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}"

engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()

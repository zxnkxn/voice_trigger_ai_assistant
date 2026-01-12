from server.db.database import engine
from server.db.models import Base

Base.metadata.create_all(bind=engine)

print("DB initialized")

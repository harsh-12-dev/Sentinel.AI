from backend.database.connection import engine, Base
from backend.database.models import ScanHistory


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("Database tables created successfully.")
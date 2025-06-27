from sqlmodel import SQLModel, create_engine, Session

# SQLite database file
DATABASE_URL = "sqlite:///./tasks.db"

# Create the engine
engine = create_engine(DATABASE_URL, echo=True)  # echo=True for logging SQL

# Create the DB + tables (called from main.py at startup)
def init_db():
    SQLModel.metadata.create_all(engine)

# Dependency for getting a DB session
def get_session():
    with Session(engine) as session:
        yield session
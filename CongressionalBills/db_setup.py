import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load environment variables
load_dotenv()

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL")
Base = declarative_base()

class Bill(Base):
    __tablename__ = "bills"
    id = Column(Integer, primary_key=True, autoincrement=True)
    bill_id = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    summary = Column(Text)
    plain_language_summary = Column(Text)
    expenditures = Column(Text)  # Stored as a JSON string
    processed = Column(Boolean, default=False)

# Setup database
def init_db():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)

Session = init_db()

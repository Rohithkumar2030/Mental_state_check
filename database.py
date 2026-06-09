import os
from dotenv import load_dotenv
import urllib.parse
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, text
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()
PASSWORD=os.getenv("MYSQL_PASSWORD")
# for Safely encode special characters (like @, :, /, etc.) in the password
ENCODED_PASSWORD = urllib.parse.quote_plus(PASSWORD)
DATABASE_URL = f"mysql+mysqlconnector://root:{ENCODED_PASSWORD}@localhost/Mental_Health"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- ORM Models ---

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(50), nullable=False)

class Issue(Base):
    __tablename__ = "issues"
    issue_id = Column(Integer, primary_key=True, autoincrement=True)
    issue = Column(String(200), nullable=False)

class Question(Base):
    __tablename__ = "questions"
    question_id = Column(Integer, primary_key=True, autoincrement=True)
    issue_id = Column(Integer, ForeignKey("issues.issue_id"))
    question_text = Column(String(200), nullable=False)
    question_order = Column(Integer)

class Choice(Base):
    __tablename__ = "choices"
    choice_id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey("questions.question_id"))
    choice_text = Column(String(200), nullable=False)
    score = Column(Integer)
    choice_order = Column(Integer)

class Submission(Base):
    __tablename__ = "submissions"
    submission_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    issue_id = Column(Integer, ForeignKey("issues.issue_id"))
    total_score = Column(Integer)
    severity_band = Column(String(25))

class SubmissionAnswer(Base):
    __tablename__ = "submission_answers"
    submission_answers_id = Column(Integer, primary_key=True, autoincrement=True)
    submission_id = Column(Integer, ForeignKey("submissions.submission_id"))
    question_id = Column(Integer, ForeignKey("questions.question_id"))
    choice_id = Column(Integer, ForeignKey("choices.choice_id"))
    awarded_score = Column(Integer)

class Suggestion(Base):
    __tablename__ = "suggestions"
    suggestion_id = Column(Integer, primary_key=True, autoincrement=True)
    issue_id = Column(Integer, ForeignKey("issues.issue_id"))
    severity_band = Column(String(25))
    suggestion = Column(String(200), nullable=False)

# Create tables if they do not exist
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

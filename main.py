from fastapi import FastAPI, Depends, Form, HTTPException, Request, status
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import Annotated
from pydantic import BaseModel, Field
from datetime import datetime

from database import get_db, User, Issue, Question, Choice, SubmissionAnswer, Submission, Suggestion

app = FastAPI()
templates = Jinja2Templates(directory="static/templates")
app.add_middleware(
    SessionMiddleware,
    secret_key="sjdfsjdfjasdjgdgjhwjdgwtegjk"  # Change this to a secure random string
)

class UserCreate(BaseModel):
    user_name: str = Field(min_length=3, max_length=50)

    @classmethod
    def as_form(cls, user_name: Annotated[str, Form(...)]):
        """converts html form data to validated pydentic field data"""
        return cls(user_name=user_name)

class SubmissionIssueCreate(BaseModel):
    issue_id: int

    @classmethod
    def as_form(cls, issue_id: Annotated[int, Form(...)]):
        return cls(issue_id=issue_id)

class SubmissionAnswerCreate(BaseModel):
    choice_id: int
    awarded_score: int

class SubmissionAnswerUpdate(BaseModel):
    choice_id: int | None = None
    awarded_score: int | None = None

class SubmissionFinalCreate(BaseModel):
    final_submitted_at: datetime

@app.get('/', response_class=Jinja2Templates)
async def root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

# POST /users -- users submit the names
@app.post("/users")
# Injecting the validated model using Depends
async def create_users(
    request: Request,
    user_data: Annotated[UserCreate, Depends(UserCreate.as_form)],
    db: Session = Depends(get_db)):

    try:
        # Save to Database using SQLAlchemy
        new_user = User(user_name=user_data.user_name.strip())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        # save user id to the request session
        request.session["user_id"] = new_user.user_id
        return RedirectResponse(url="/issues", status_code=303)
    except Exception as e:
        db.rollback()
        # Log error internally, show generic message to user
        print(f"DB Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to save user.")


# GET /users/{user_id} -- user get the his profile details(name)
@app.get("/users/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": user.user_id, "user_name": user.user_name}

# GET /issues -- user gets all the issue options
@app.get("/issues", response_class=Jinja2Templates)
async def get_issues(request: Request, db: Session = Depends(get_db)):
    issue = db.query(Issue).all()
    if not issue:
        raise HTTPException(status_code=404, detail="issue not found")
    return templates.TemplateResponse("issue.html", {"request": request, "issues": issue})

# POST /submissions/ -- user makes his first submission ie his issue submission
@app.post("/submissions")
async def create_submission(
    request: Request,
    submission_data: Annotated[SubmissionIssueCreate, Depends(SubmissionIssueCreate.as_form)],
    db: Session = Depends(get_db)):

    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User session not found. Please log in again."
        )

    try:
        # Save to Database using SQLAlchemy
        new_submission = Submission(user_id=user_id, issue_id=submission_data.issue_id, total_score = 0, severity_band="Pending")
        db.add(new_submission)
        db.commit()
        db.refresh(new_submission)
        return RedirectResponse(url=f"/submissions/{new_submission.submission_id}/questions", status_code=303)
    except Exception as e:
        db.rollback()
        # Log error internally, show generic message to user
        print(f"DB Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to save submission")


# GET /submissions/{submission_id}/questions -- user gets all his questions
@app.get("/submissions/{submission_id}/questions")
async def get_submission_questions(submission_id: int):

    return {"submission_id": submission_id, "questions": []}

# GET /submissions/{submission_id}/questions/{question_id}/choices -- user gets his each questions displayed
@app.get("/submissions/{submission_id}/questions/{question_id}")
async def get_question(submission_id: int, question_id: int):
    return {"submission_id": submission_id, "question_id": question_id, "question": []}

# GET /submissions/{submission_id}/questions/{question_id}/choices -- user can get his options
@app.get("/submissions/{submission_id}/questions/{question_id}/choices")
async def get_choices(submission_id: int, question_id: int):
    return {"submission_id": submission_id, "question_id": question_id, "choices": []}

# POST /submissions/{submission_id}/submission_answers -- user can submit his options
@app.post("/submissions/{submission_id}/questions/{question_id}/submission_answers")
async def create_answer_submission(submission_id: int, question_id: int, payload: SubmissionAnswerCreate):
    return {"message": "submission Answer created", "submission_id": submission_id, "question_id": question_id, "data": payload}

# PATCH /submissions/{submission_id}/questions/{question_id}/submission_answers/{submission_answers_id} -- user can update his answers
@app.patch("/submissions/{submission_id}/questions/{question_id}/submission_answers/{submission_answers_id}")
async def update_answer_submission(submission_id: int, question_id: int, submission_answers_id: int, payload: SubmissionAnswerUpdate):
    return {"message": "submission updated", "submission_id": submission_id, "data": payload}

# POST /submissions/{submission_id}/submission_answers -- user can submit his entire quiz
@app.post("/submissions/{submission_id}/submission_answers")
async def create_final_submission(submission_id: int, payload: SubmissionFinalCreate):
    return {"message": "final submission created", "submission_id": submission_id, "data": payload}

# GET /submissions/{submission_id}/score -- user can get his score
@app.get("/submissions/{submission_id}/score")
async def get_score(submission_id: int):
    return {"submission_id": submission_id, "score": 0, "severity_band": "Pending"}

# GET /submissions/{submission_id}/suggestions -- user can get his suggestions
@app.get("/submissions/{submission_id}/suggestions")
async def get_suggestions(submission_id: int):
    return {"submission_id": submission_id, "suggestions": []}

# Submitted questions are same as questions
# # GET /submissions/{submission_id}/questions/{question_id} -- user can get his questions for review
# @app.get("/submissions/{submission_id}/questions/{question_id}")
# async def get_submitted_questions(submission_id: int, question_id: int):
#     return {"submission_id": submission_id, "question_id": question_id, "questions": []}

# GET /submissions/{submission_id}/submission_answers/{submission_answers_id} -- user can get his answers for review
@app.get("/submissions/{submission_id}/submission_answers/{submission_answers_id}")
async def get_submitted_answers(submission_id: int, submission_answers_id: int):
    return {"submission_id": submission_id, "submission_answers_id": submission_answers_id, "submission_answer": [] }


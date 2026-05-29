from fastapi import FastAPI, HTTPException
from database import cnx, Tables
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

class UserCreate(BaseModel):
    user_name: str

class SubmissionIssueCreate(BaseModel):
    user_id: int
    issue_id: int

class SubmissionAnswerCreate(BaseModel):
    choice_id: int
    awarded_score: int

class SubmissionAnswerUpdate(BaseModel):
    choice_id: int | None = None
    awarded_score: int | None = None

class SubmissionFinalCreate(BaseModel):
    final_submitted_at: datetime

@app.get('/')
async def root():
    return {"message": "My app is running"}

# POST /users -- users submit the names
@app.post("/users")
async def create_users(payload: UserCreate):
    return {"message": "user created", "data": payload}

# GET /users/{user_id} -- user get the his profile details(name)
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}

# GET /issues -- user gets the issue options for the user
@app.get("/issues")
async def get_issues():
    return {"issues": []}

# POST /submissions/ -- user makes his first submission ie his issue submission
@app.post("/submissions")
async def create_submission(payload: SubmissionIssueCreate):
    return {"message": "submission created", "data": payload}

# GET /submissions/{submission_id}/questions -- user gets all his questions
@app.get("/submissions/{submission_id}/questions")
async def get_submission_questions(submission_id: int):
    return {"submission_id": submission_id, "questions": []}

# GET /submissions/{submission_id}/questions/{question_id}/choices -- user gets his each questions displayed
@app.get("/submissions/{submission_id}/questions/{question_id}")
async def get_question(submission_id: int, question_id: int):
    return {"submission_id": submission_id, "question_id": question_id, "question": []}

# POST /submissions/{submission_id}/questions/{question_id}/submission_answers -- user can get his options
@app.get("/submissions/{submission_id}/questions/{question_id}/choices")
async def get_choices(submission_id: int, question_id: int):
    return {"submission_id": submission_id, "question_id": question_id, "choices": []}

# POST /submissions/{submission_id}/submission_answers -- user can submit his options
@app.post("/submissions/{submission_id}/questions/{question_id}/submission_answers")
async def create_answer_submission(payload: SubmissionAnswerCreate):
    return {"message": "submission Answer created", "data": payload}

# PATCH /submissions/{submission_id}/questions/{question_id}/submission_answers/{submission_answers_id} -- user can update his answers
@app.patch("/submissions/{submission_id}/questions/{question_id}/submission_answers/{submission_answers_id}")
async def update_answer_submission(submission_id: int, question_id: int, submission_answers_id: int, payload: SubmissionAnswerUpdate):
    return {"message": "submission updated", "submission_id": submission_id, "data": payload}

# POST /submissions/{submission_id}/submission_answers -- user can submit his quiz
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

# GET /submissions/{submission_id}/questions/{question_id} -- user can get his questions for review
@app.get("/submissions/{submission_id}/questions/{question_id}")
async def get_submitted_questions(submission_id: int, question_id: int):
    return {"submission_id": submission_id, "question_id": question_id, "questions": []}

# GET /submissions/{submission_id}/submission_answers/{submission_answers_id} -- user can get his answers for review
@app.get("/submissions/{submission_id}/submission_answers/{submission_answers_id}")
async def get_submitted_answers(submission_id: int, submission_answers_id: int):
    return {"submission_id": submission_id, "submission_answers_id": submission_answers_id, "submission_answer": [] }

cursor = cnx.cursor()

for name in ["users","issues","questions","choices","submissions","submission_answers","suggestions"]:
    cursor.execute(Tables[name])

cnx.commit()
cursor.close()
cnx.close()
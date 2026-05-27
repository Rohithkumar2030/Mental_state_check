from fastapi import FastAPI
from database import cnx, Tables
app = FastAPI()

@app.get('/')
async def root():
    return {"message": "Hello the World"}


cursor = cnx.cursor()

for name in ["users","issues","questions","options","submissions","submission_answers","suggestions"]:
    cursor.execute(Tables[name])


cnx.commit()
cursor.close()
cnx.close()
# @app.get('/')
# async def questions():
#     return request.get(problems.html)

# @app.get('/questions')

# @app.get('/ready')

# @app.get('/condition')
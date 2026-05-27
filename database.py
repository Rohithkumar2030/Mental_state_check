import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()
password=os.getenv("MYSQL_PASSWORD")
cnx = mysql.connector.connect(user='root', password= password, database='Mental_Health')

Tables= {}
Tables["users"] = """CREATE TABLE IF NOT EXISTS users(
    user_id INT AUTO_INCREMENT PRIMARY KEY ,
    user_name VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"""

Tables["issues"] = """CREATE TABLE IF NOT EXISTS issues(
    issue_id INT AUTO_INCREMENT PRIMARY KEY,
    issue VARCHAR(200))"""

Tables["questions"] = """CREATE TABLE IF NOT EXISTS questions(
    question_id INT AUTO_INCREMENT PRIMARY KEY,
    issue_id INT,
    question_text VARCHAR(200),
    question_order INT,
    FOREIGN KEY (issue_id) REFERENCES issues(issue_id))"""

Tables["options"] = """CREATE TABLE IF NOT EXISTS options (
    option_id INT AUTO_INCREMENT PRIMARY KEY,
    question_id INT,
    option_text VARCHAR(200),
    score INT,
    option_order INT,
    FOREIGN KEY (question_id) REFERENCES questions(question_id))"""

Tables["submissions"] = """CREATE TABLE IF NOT EXISTS submissions (
    submission_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    issue_id INT,
    total_score INT,
    severity_band VARCHAR(25),
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (issue_id) REFERENCES issues(issue_id))"""

Tables["submission_answers"] = """CREATE TABLE IF NOT EXISTS submission_answers (
    submission_answers_id INT AUTO_INCREMENT PRIMARY KEY,
    submission_id INT,
    question_id INT,
    option_id INT,
    awarded_score INT,
    FOREIGN KEY (submission_id) REFERENCES submissions(submission_id),
    FOREIGN KEY (question_id) REFERENCES questions(question_id),
    FOREIGN KEY (option_id) REFERENCES options(option_id))"""

Tables["suggestions"]="""CREATE TABLE IF NOT EXISTS suggestions (
    suggestion_id INT AUTO_INCREMENT PRIMARY KEY,
    issue_id INT,
    severity_band VARCHAR(25),
    suggestion VARCHAR(200),
    FOREIGN KEY (issue_id) REFERENCES issues(issue_id))"""


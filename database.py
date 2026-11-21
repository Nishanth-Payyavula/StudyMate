
import sqlite3
import os
from contextlib import closing

DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "studymate.db")

# Connect to our database
def get_connection():
    return sqlite3.connect(DATABASE_PATH)


# Create tables if they don't exist
def initialize_database():

    with closing(get_connection()) as connection:
        cursor = connection.cursor()

        # Notes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL
            )
        """)

        # Tasks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                subject TEXT NOT NULL,
                completed INTEGER DEFAULT 0
            )
        """)

        # Quiz Questions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quiz_questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                question TEXT NOT NULL,
                option_a TEXT NOT NULL,
                option_b TEXT NOT NULL,
                option_c TEXT NOT NULL,
                option_d TEXT NOT NULL,
                correct_answer TEXT NOT NULL,
                explanation TEXT,
                difficulty TEXT DEFAULT 'Easy',
                created_by TEXT DEFAULT 'system'
            )
        """)

        # Quiz Attempts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quiz_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                score INTEGER NOT NULL,
                total_questions INTEGER NOT NULL,
                attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        connection.commit()


# Save a note
def add_note(subject, title, content):

    with closing(get_connection()) as connection:
        connection.execute(
            "INSERT INTO notes (subject, title, content) VALUES (?, ?, ?)",
            (subject, title, content)
        )

        connection.commit()


# Read all notes
def get_notes():

    with closing(get_connection()) as connection:
        cursor = connection.execute(
            "SELECT id, subject, title, content FROM notes"
        )

        notes = cursor.fetchall()

    return notes


# Delete a note
def delete_note(note_id):

    with closing(get_connection()) as connection:
        connection.execute(
            "DELETE FROM notes WHERE id = ?",
            (note_id,)
        )

        connection.commit()


# Add a task
def add_task(name, subject):

    with closing(get_connection()) as connection:
        connection.execute(
            "INSERT INTO tasks (name, subject) VALUES (?, ?)",
            (name, subject)
        )

        connection.commit()


# Get all tasks
def get_tasks():

    with closing(get_connection()) as connection:
        cursor = connection.execute(
            "SELECT id, name, subject, completed FROM tasks"
        )

        tasks = cursor.fetchall()

    return tasks


# Mark a task complete
def complete_task(task_id):

    with closing(get_connection()) as connection:
        connection.execute(
            "UPDATE tasks SET completed = 1 WHERE id = ?",
            (task_id,)
        )

        connection.commit()


def add_quiz_question(subject, question, option_a, option_b, option_c, option_d,
                      correct_answer, explanation="", difficulty="Easy",
                      created_by="system"):

    required_text = {
        "subject": subject,
        "question": question,
        "option_a": option_a,
        "option_b": option_b,
        "option_c": option_c,
        "option_d": option_d,
    }

    for field_name, value in required_text.items():
        if not isinstance(value, str) or not value.strip():
            raise ValueError(field_name + " is required.")

    if not isinstance(correct_answer, str):
        raise ValueError("correct_answer must be A, B, C, or D.")

    correct_answer = correct_answer.strip().upper()
    if correct_answer not in ("A", "B", "C", "D"):
        raise ValueError("correct_answer must be A, B, C, or D.")

    with closing(get_connection()) as connection:
        connection.execute(
            """
            INSERT INTO quiz_questions (
                subject, question, option_a, option_b, option_c, option_d,
                correct_answer, explanation, difficulty, created_by
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                subject, question, option_a, option_b, option_c, option_d,
                correct_answer, explanation, difficulty, created_by
            )
        )

        connection.commit()


def get_quiz_questions(subject=None, difficulty=None, limit=None):

    query = """
        SELECT id, subject, question, option_a, option_b, option_c, option_d,
               correct_answer, explanation, difficulty, created_by
        FROM quiz_questions
    """
    conditions = []
    parameters = []

    if subject is not None:
        if not isinstance(subject, str) or not subject.strip():
            raise ValueError("subject must be a non-empty string.")
        conditions.append("subject = ?")
        parameters.append(subject)

    if difficulty is not None:
        if not isinstance(difficulty, str) or not difficulty.strip():
            raise ValueError("difficulty must be a non-empty string.")
        conditions.append("difficulty = ?")
        parameters.append(difficulty)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY id"

    if limit is not None:
        if isinstance(limit, bool) or not isinstance(limit, int) or limit < 0:
            raise ValueError("limit must be a non-negative integer.")
        query += " LIMIT ?"
        parameters.append(limit)

    with closing(get_connection()) as connection:
        cursor = connection.execute(query, parameters)
        questions = cursor.fetchall()

    return questions


def save_quiz_attempt(subject, score, total_questions):

    if not isinstance(subject, str) or not subject.strip():
        raise ValueError("subject is required.")
    if isinstance(score, bool) or not isinstance(score, int) or score < 0:
        raise ValueError("score must be a non-negative integer.")
    if (isinstance(total_questions, bool)
            or not isinstance(total_questions, int)
            or total_questions < 0):
        raise ValueError("total_questions must be a non-negative integer.")
    if score > total_questions:
        raise ValueError("score cannot exceed total_questions.")

    with closing(get_connection()) as connection:
        connection.execute(
            """
            INSERT INTO quiz_attempts (subject, score, total_questions)
            VALUES (?, ?, ?)
            """,
            (subject, score, total_questions)
        )

        connection.commit()


def get_quiz_attempts(subject=None, limit=20):

    if subject is not None and (
            not isinstance(subject, str) or not subject.strip()):
        raise ValueError("subject must be a non-empty string.")
    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 0:
        raise ValueError("limit must be a non-negative integer.")

    query = """
        SELECT id, subject, score, total_questions, attempted_at
        FROM quiz_attempts
    """
    parameters = []

    if subject is not None:
        query += " WHERE subject = ?"
        parameters.append(subject)

    query += " ORDER BY attempted_at DESC, id DESC LIMIT ?"
    parameters.append(limit)

    with closing(get_connection()) as connection:
        cursor = connection.execute(query, parameters)
        attempts = cursor.fetchall()

    return attempts


# Initialize our database
initialize_database()
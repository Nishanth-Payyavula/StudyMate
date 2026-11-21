
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


# Initialize our database
initialize_database()
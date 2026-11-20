import sqlite3

# Connect to our database
def get_connection():
    return sqlite3.connect("studymate.db")


# Create tables if they don't exist
def initialize_database():

    connection = get_connection()
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

    connection.commit()
    connection.close()


# Save a note
def add_note(subject, title, content):

    connection = get_connection()

    connection.execute(
        "INSERT INTO notes (subject, title, content) VALUES (?, ?, ?)",
        (subject, title, content)
    )

    connection.commit()
    connection.close()


# Read all notes
def get_notes():

    connection = get_connection()

    cursor = connection.execute(
        "SELECT id, subject, title, content FROM notes"
    )

    notes = cursor.fetchall()

    connection.close()

    return notes


# Delete a note
def delete_note(note_id):

    connection = get_connection()

    connection.execute(
        "DELETE FROM notes WHERE id = ?",
        (note_id,)
    )

    connection.commit()
    connection.close()


# Add a task
def add_task(name, subject):

    connection = get_connection()

    connection.execute(
        "INSERT INTO tasks (name, subject) VALUES (?, ?)",
        (name, subject)
    )

    connection.commit()
    connection.close()


# Get all tasks
def get_tasks():

    connection = get_connection()

    cursor = connection.execute(
        "SELECT id, name, subject, completed FROM tasks"
    )

    tasks = cursor.fetchall()

    connection.close()

    return tasks


# Mark a task complete
def complete_task(task_id):

    connection = get_connection()

    connection.execute(
        "UPDATE tasks SET completed = 1 WHERE id = ?",
        (task_id,)
    )

    connection.commit()
    connection.close()


# Initialize our database
initialize_database()
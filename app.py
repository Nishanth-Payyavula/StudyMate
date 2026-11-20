import streamlit as st

from database import (
    add_note,
    get_notes,
    delete_note,
    add_task,
    get_tasks,
    complete_task
)

# --------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="StudyMate",
    page_icon="📚",
    layout="wide"
)

# --------------------------------
# 2. SIDEBAR
# --------------------------------

st.sidebar.title("📚 StudyMate")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "My Notes", "Study Planner", "Quiz"]
)

st.sidebar.divider()
st.sidebar.caption("Version 0.3 | SQLite Database")


# --------------------------------
# 3. DASHBOARD
# --------------------------------

if page == "Dashboard":

    st.title("🏠 Dashboard")
    st.write("Welcome to your personal study space!")

    # Get actual data from database
    notes = get_notes()
    tasks = get_tasks()

    completed_count = sum(task[3] for task in tasks)

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Notes", len(notes))
    col2.metric("Total Tasks", len(tasks))
    col3.metric("Completed Tasks", completed_count)

    st.divider()

    st.subheader("🚀 Quick Start")

    st.write("Use the sidebar to navigate through your application.")

    st.info("Your notes and tasks are now stored in a database!")


# --------------------------------
# 4. MY NOTES
# --------------------------------

elif page == "My Notes":

    st.title("📝 My Notes")

    with st.form("note_form"):

        subject = st.text_input("Subject")

        note_title = st.text_input("Note Title")

        note_content = st.text_area(
            "Write your note here",
            height=150
        )

        submitted = st.form_submit_button("Save Note")

        if submitted:

            if subject and note_title and note_content:

                add_note(subject, note_title, note_content)

                st.success("Note saved successfully!")

            else:

                st.warning("Please fill in all fields.")

    st.divider()

    st.subheader("📚 Your Saved Notes")

    notes = get_notes()

    search = st.text_input("🔍 Search notes")

    filtered_notes = []

    for note in notes:

        note_id, subject, title, content = note

        searchable_text = subject + title + content

        if search.lower() in searchable_text.lower():

            filtered_notes.append(note)

    for note in filtered_notes:

        note_id, subject, title, content = note

        with st.expander(f"{subject} — {title}"):

            st.write(content)

            if st.button(
                "🗑️ Delete Note",
                key=f"delete_note_{note_id}"
            ):

                delete_note(note_id)

                st.rerun()

    if not notes:

        st.info("You haven't created any notes yet.")

    elif not filtered_notes:

        st.warning("No notes match your search.")


# --------------------------------
# 5. STUDY PLANNER
# --------------------------------

elif page == "Study Planner":

    st.title("✅ Study Planner")

    with st.form("task_form"):

        task_name = st.text_input("Task Name")

        task_subject = st.text_input("Subject")

        submitted = st.form_submit_button("Add Task")

        if submitted:

            if task_name and task_subject:

                add_task(task_name, task_subject)

                st.success("Task added successfully!")

            else:

                st.warning("Enter both task name and subject.")

    st.divider()

    st.subheader("📋 Your Tasks")

    tasks = get_tasks()

    for task in tasks:

        task_id, name, subject, completed = task

        col1, col2 = st.columns([4, 1])

        with col1:

            if completed:

                st.write(f"✅ ~~{name}~~ — {subject}")

            else:

                st.write(f"⏳ **{name}** — {subject}")

        with col2:

            if not completed:

                if st.button(
                    "Complete",
                    key=f"complete_task_{task_id}"
                ):

                    complete_task(task_id)

                    st.rerun()

    if not tasks:

        st.info("No tasks yet. Add your first task!")


# --------------------------------
# 6. QUIZ
# --------------------------------

elif page == "Quiz":

    st.title("🧠 Quiz")

    st.info(
        "Quiz functionality is coming soon! "
        "We'll build an interactive quiz system next."
    )
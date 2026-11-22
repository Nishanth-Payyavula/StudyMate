import random
import sqlite3

import streamlit as st

from database import (
    add_note,
    get_notes,
    delete_note,
    add_task,
    get_tasks,
    complete_task,
    get_quiz_questions,
    save_quiz_attempt,
    get_quiz_attempts
)

QUIZ_SUBJECTS = [
    "Python",
    "Artificial Intelligence & Machine Learning",
    "AWS & Cloud Computing",
    "Database Management Systems",
    "Computer Networks",
    "Operating Systems",
    "General Knowledge",
    "Mathematics",
    "Physics",
    "Chemistry",
]

QUIZ_DIFFICULTIES = ["Easy", "Medium", "Hard", "Mixed"]


def prepare_quiz_question(question_row):
    (
        question_id, subject, question, option_a, option_b, option_c, option_d,
        correct_answer, explanation, difficulty, _created_by
    ) = question_row

    original_options = [
        ("A", option_a),
        ("B", option_b),
        ("C", option_c),
        ("D", option_d),
    ]

    required_text = [subject, question, option_a, option_b, option_c, option_d]
    if any(
        not isinstance(value, str) or not value.strip()
        for value in required_text
    ):
        raise ValueError("A quiz question is missing required text.")
    if not isinstance(correct_answer, str):
        raise ValueError("A quiz question has an invalid correct answer.")

    correct_answer = correct_answer.strip().upper()
    if correct_answer not in ("A", "B", "C", "D"):
        raise ValueError("A quiz question has an invalid correct answer.")

    random.shuffle(original_options)

    display_options = {}
    display_correct_answer = None
    for index, (original_label, option_text) in enumerate(original_options):
        display_label = chr(ord("A") + index)
        display_options[display_label] = option_text
        if original_label == correct_answer:
            display_correct_answer = display_label

    return {
        "id": question_id,
        "subject": subject,
        "question": question,
        "options": display_options,
        "correct_answer": display_correct_answer,
        "explanation": explanation or "No explanation is available.",
        "difficulty": difficulty or "Easy",
    }


def reset_quiz_state():
    st.session_state["quiz_active"] = False
    st.session_state["quiz_questions"] = []
    st.session_state["quiz_index"] = 0
    st.session_state["quiz_score"] = 0
    st.session_state["quiz_answered"] = False
    st.session_state["quiz_is_correct"] = False
    st.session_state["quiz_selected_answer"] = None
    st.session_state["quiz_attempt_subject"] = ""
    st.session_state["quiz_attempt_saved"] = False
    st.session_state["quiz_attempt_save_error"] = None
    st.session_state["quiz_completed_score"] = None
    st.session_state["quiz_completed_total"] = None


def save_completed_quiz_attempt():
    if st.session_state["quiz_attempt_saved"]:
        return

    try:
        save_quiz_attempt(
            st.session_state["quiz_attempt_subject"],
            st.session_state["quiz_completed_score"],
            st.session_state["quiz_completed_total"],
        )
    except (sqlite3.Error, ValueError) as error:
        st.session_state["quiz_attempt_save_error"] = str(error)
    else:
        st.session_state["quiz_attempt_saved"] = True
        st.session_state["quiz_attempt_save_error"] = None


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

    st.title("🧠 StudyMate Quiz")
    st.write("Choose a quiz mode, set your subject and difficulty, then test your knowledge.")

    quiz_defaults = {
        "quiz_active": False,
        "quiz_questions": [],
        "quiz_index": 0,
        "quiz_score": 0,
        "quiz_answered": False,
        "quiz_is_correct": False,
        "quiz_selected_answer": None,
        "quiz_attempt_subject": "",
        "quiz_attempt_saved": False,
        "quiz_attempt_save_error": None,
        "quiz_completed_score": None,
        "quiz_completed_total": None,
        "quiz_run_id": 0,
    }
    for state_key, default_value in quiz_defaults.items():
        if state_key not in st.session_state:
            st.session_state[state_key] = default_value

    if not st.session_state["quiz_active"]:
        mode = st.selectbox(
            "Quiz mode",
            ["Subject-wise Quiz", "Quick Challenge", "Exam Challenge"],
        )

        selection_col, difficulty_col = st.columns(2)
        with selection_col:
            if mode == "Subject-wise Quiz":
                selected_scope = st.selectbox("Subject", QUIZ_SUBJECTS)
                question_subject = selected_scope
                attempt_subject = selected_scope
            else:
                selected_scope = st.selectbox(
                    "Question scope",
                    ["All Subjects"] + QUIZ_SUBJECTS,
                )
                question_subject = (
                    None if selected_scope == "All Subjects" else selected_scope
                )
                attempt_subject = (
                    "Mixed" if question_subject is None else question_subject
                )

        with difficulty_col:
            selected_difficulty = st.selectbox(
                "Difficulty",
                QUIZ_DIFFICULTIES,
            )

        question_difficulty = (
            None if selected_difficulty == "Mixed" else selected_difficulty
        )

        required_count = None
        if mode == "Quick Challenge":
            required_count = 5
        elif mode == "Exam Challenge":
            required_count = 10

        question_load_error = None
        try:
            available_questions = get_quiz_questions(
                subject=question_subject,
                difficulty=question_difficulty,
            )
        except (sqlite3.Error, ValueError) as error:
            available_questions = []
            question_load_error = str(error)
            st.error("Could not load quiz questions: " + question_load_error)

        can_start = bool(available_questions)
        if question_load_error:
            can_start = False
        elif not available_questions:
            st.info(
                "No questions are available for this selection. "
                "Try another subject or difficulty, or add questions to the quiz bank."
            )
        elif required_count is not None and len(available_questions) < required_count:
            can_start = False
            st.warning(
                f"This selection has {len(available_questions)} questions, "
                f"but {required_count} are needed for {mode}."
            )
        elif required_count is not None:
            st.caption(
                f"{len(available_questions)} matching questions are available; "
                f"{required_count} will be selected at random."
            )
        else:
            st.caption(
                f"{len(available_questions)} matching questions will be asked "
                "in a random order."
            )

        if st.button("Start Quiz", type="primary", disabled=not can_start):
            try:
                selected_questions = list(available_questions)
                if required_count is not None:
                    selected_questions = random.sample(
                        selected_questions,
                        required_count,
                    )
                else:
                    random.shuffle(selected_questions)

                prepared_questions = [
                    prepare_quiz_question(row) for row in selected_questions
                ]
            except (TypeError, ValueError) as error:
                st.error("Could not prepare the selected questions: " + str(error))
            else:
                st.session_state["quiz_questions"] = prepared_questions
                st.session_state["quiz_index"] = 0
                st.session_state["quiz_score"] = 0
                st.session_state["quiz_answered"] = False
                st.session_state["quiz_is_correct"] = False
                st.session_state["quiz_selected_answer"] = None
                st.session_state["quiz_attempt_subject"] = attempt_subject
                st.session_state["quiz_attempt_saved"] = False
                st.session_state["quiz_attempt_save_error"] = None
                st.session_state["quiz_completed_score"] = None
                st.session_state["quiz_completed_total"] = None
                st.session_state["quiz_run_id"] += 1
                st.session_state["quiz_active"] = True
                st.rerun()

    else:
        questions = st.session_state["quiz_questions"]
        question_index = st.session_state["quiz_index"]
        total_questions = len(questions)

        if (
            not questions
            or question_index < 0
            or question_index >= total_questions
        ):
            st.error("The current quiz state is invalid. Please start a new quiz.")
            if st.button("Return to Quiz Setup"):
                reset_quiz_state()
                st.rerun()
        else:
            current_question = questions[question_index]
            st.progress(
                (question_index + 1) / total_questions,
                text=f"Question {question_index + 1} of {total_questions}",
            )
            st.caption(
                f"{current_question['subject']} · {current_question['difficulty']}"
            )
            st.subheader(current_question["question"])

            if not st.session_state["quiz_answered"]:
                option_labels = list(current_question["options"])
                with st.form(
                    f"quiz_answer_form_{st.session_state['quiz_run_id']}_{question_index}"
                ):
                    selected_answer = st.radio(
                        "Select your answer",
                        option_labels,
                        format_func=lambda label: (
                            f"{label}. {current_question['options'][label]}"
                        ),
                        key=(
                            f"quiz_answer_{st.session_state['quiz_run_id']}_"
                            f"{question_index}"
                        ),
                    )
                    submitted = st.form_submit_button(
                        "Submit Answer",
                        type="primary",
                    )

                if submitted:
                    is_correct = (
                        selected_answer == current_question["correct_answer"]
                    )
                    st.session_state["quiz_selected_answer"] = selected_answer
                    st.session_state["quiz_is_correct"] = is_correct
                    st.session_state["quiz_answered"] = True
                    if is_correct:
                        st.session_state["quiz_score"] += 1

                    if question_index == total_questions - 1:
                        st.session_state["quiz_completed_score"] = (
                            st.session_state["quiz_score"]
                        )
                        st.session_state["quiz_completed_total"] = total_questions
                        save_completed_quiz_attempt()

                    st.rerun()

            else:
                selected_answer = st.session_state["quiz_selected_answer"]
                if st.session_state["quiz_is_correct"]:
                    st.success("Correct! Well done.")
                else:
                    correct_label = current_question["correct_answer"]
                    correct_text = current_question["options"][correct_label]
                    st.error(
                        f"Not quite. The correct answer is "
                        f"{correct_label}. {correct_text}"
                    )

                st.info("Explanation: " + current_question["explanation"])
                st.caption(
                    "Your answer: "
                    f"{selected_answer}. "
                    f"{current_question['options'][selected_answer]}"
                )

                if question_index < total_questions - 1:
                    if st.button("Next Question", type="primary"):
                        st.session_state["quiz_index"] += 1
                        st.session_state["quiz_answered"] = False
                        st.session_state["quiz_is_correct"] = False
                        st.session_state["quiz_selected_answer"] = None
                        st.rerun()
                else:
                    if st.session_state["quiz_completed_score"] is None:
                        st.session_state["quiz_completed_score"] = (
                            st.session_state["quiz_score"]
                        )
                    if st.session_state["quiz_completed_total"] is None:
                        st.session_state["quiz_completed_total"] = total_questions

                    percentage = (
                        st.session_state["quiz_completed_score"]
                        / st.session_state["quiz_completed_total"]
                    ) * 100
                    st.divider()
                    st.subheader("Quiz Results")
                    result_col1, result_col2 = st.columns(2)
                    result_col1.metric(
                        "Score",
                        f"{st.session_state['quiz_completed_score']} / "
                        f"{st.session_state['quiz_completed_total']}",
                    )
                    result_col2.metric("Percentage", f"{percentage:.1f}%")

                    if st.session_state["quiz_attempt_saved"]:
                        st.success("Your attempt was saved to quiz history.")
                    elif st.session_state["quiz_attempt_save_error"]:
                        st.error(
                            "Your result could not be saved: "
                            + st.session_state["quiz_attempt_save_error"]
                        )
                        if st.button("Retry Saving Attempt", type="primary"):
                            save_completed_quiz_attempt()
                            st.rerun()

                    if st.button("Start Another Quiz"):
                        reset_quiz_state()
                        st.rerun()

    st.divider()
    st.subheader("📊 Quiz History")
    try:
        quiz_attempts = get_quiz_attempts(limit=20)
    except (sqlite3.Error, ValueError) as error:
        st.error("Could not load quiz history: " + str(error))
    else:
        if quiz_attempts:
            history_rows = [
                {
                    "Subject": attempt[1],
                    "Score": attempt[2],
                    "Total Questions": attempt[3],
                    "Date": attempt[4],
                }
                for attempt in quiz_attempts
            ]
            st.table(history_rows)
        else:
            st.info("No quiz attempts yet. Complete a quiz to see your history here.")
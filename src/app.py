import streamlit as st
import pandas as pd
import subprocess
import os
from datetime import datetime
from tasks import load_tasks, save_tasks, filter_tasks_by_priority, filter_tasks_by_category, generate_unique_id, get_overdue_tasks, search_tasks, summarize_by_category

def main():
    st.title("To-Do Application")

    # Load existing tasks
    tasks = load_tasks()

    # Sidebar for adding new tasks
    st.sidebar.header("Add New Task")

    # Task creation form
    with st.sidebar.form("new_task_form"):
        task_title = st.text_input("Task Title")
        task_description = st.text_area("Description")
        task_priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        task_category = st.selectbox("Category", ["Work", "Personal", "School", "Other"])
        task_due_date = st.date_input("Due Date")
        submit_button = st.form_submit_button("Add Task")

        if submit_button:
            if task_title:
                new_task = {
                    "id": generate_unique_id(tasks),
                    "title": task_title,
                    "description": task_description,
                    "priority": task_priority,
                    "category": task_category,
                    "due_date": task_due_date.strftime("%Y-%m-%d"),
                    "completed": False,
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                tasks.append(new_task)
                save_tasks(tasks)
                st.sidebar.success("Task added successfully!")
            else:
                st.sidebar.error("Task title cannot be empty!")

    # Main area to display tasks
    st.header("Your Tasks")
    category_summary = summarize_by_category(tasks)
    st.subheader("Task Count, Sorted by Category")
    st.write(", ".join(f"{cat}: {count}" for cat, count in category_summary.items()))

    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        filter_category = st.selectbox("Filter by Category", ["All"] + list(set([task["category"] for task in tasks])))
    with col2:
        filter_priority = st.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])

    show_completed = st.checkbox("Show Completed Tasks")
    show_overdue = st.checkbox("Show Only Overdue Tasks")
    search_query = st.text_input("Search Tasks")



    # Apply filters
    filtered_tasks = tasks.copy()
    if filter_category != "All":
        filtered_tasks = filter_tasks_by_category(filtered_tasks, filter_category)
    if filter_priority != "All":
        filtered_tasks = filter_tasks_by_priority(filtered_tasks, filter_priority)
    if show_overdue:
        filtered_tasks = get_overdue_tasks(filtered_tasks)
    if search_query:
        filtered_tasks = search_tasks(filtered_tasks, search_query)
    elif not show_completed:
        filtered_tasks = [task for task in filtered_tasks if not task["completed"]]

    # Display tasks
    for task in filtered_tasks:
        col1, col2 = st.columns([4, 1])
        with col1:
            if task["completed"]:
                st.markdown(f"~~**{task['title']}**~~")
            else:
                st.markdown(f"**{task['title']}**")
            st.write(task["description"])
            st.caption(f"Due: {task['due_date']} | Priority: {task['priority']} | Category: {task['category']}")
        with col2:
            if st.button("Complete" if not task["completed"] else "Undo", key=f"complete_{task['id']}"):
                for t in tasks:
                    if t["id"] == task["id"]:
                        t["completed"] = not t["completed"]
                        save_tasks(tasks)
                        st.rerun()
            if st.button("Delete", key=f"delete_{task['id']}"):
                tasks = [t for t in tasks if t["id"] != task["id"]]
                save_tasks(tasks)
                st.rerun()

    # ----------------------------------
    # Expanded Testing Section
    # ----------------------------------

    st.header("Testing Section")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Run Unit Tests"):
            st.write("Running Unit Tests...")
            result = subprocess.run(
                ["pytest", "tests/test_basic.py", "--cov=src", "--cov-report=term-missing"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            st.text(result.stdout)
            if result.stderr:
                st.error(result.stderr)

    with col2:
        if st.button("Run Advanced Tests"):
            st.write("Running Advanced Tests...")
            result = subprocess.run(
                ["pytest", "tests/test_advanced.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            st.text(result.stdout)
            if result.stderr:
                st.error(result.stderr)

    with col3:
        if st.button("Generate HTML Report"):
            st.write("Generating HTML Report...")
            result = subprocess.run(
                ["pytest", "tests/", "--html=report.html", "--self-contained-html"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            st.text(result.stdout)
            if result.stderr:
                st.error(result.stderr)
            
            # Offer the generated report.html as a downloadable file
            if os.path.exists("report.html"):
                with open("report.html", "rb") as f:
                    st.download_button(
                        label="Download HTML Report",
                        data=f,
                        file_name="test_report.html",
                        mime="text/html"
                    )


if __name__ == "__main__":
    main()

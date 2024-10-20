import streamlit as st
import os


# Streamlit app layout
st.set_page_config(layout="wide")
#set title at center
#st.title("C++ to Java Migration Assistant")
st.markdown("<h1 style='text-align: center;'>C++ to Java Migration Assistant</h1>", unsafe_allow_html=True)
st.sidebar.markdown("## AI4Tech POC 🎈")

# Create two columns with specified widths
col0, col1, col2 = st.columns([3, 6, 8])

# Initialize session state for status message and task output
if 'status_message' not in st.session_state:
    st.session_state['status_message'] = "Status not initialized"
if 'current_task' not in st.session_state:
    st.session_state['current_task'] = None
if 'input_file_path' not in st.session_state:
    st.session_state['input_file_path'] = None
if 'output_directory' not in st.session_state:
    st.session_state['output_directory'] = None

# Initialize session state for task statuses and outputs
if 'tasks' not in st.session_state:
    st.session_state['tasks'] = {
        'code_explanation': {
            'status': 'Not Started',  # Possible values: 'Not Started', 'In Progress', 'Completed', 'Failed'
            'output': None
        },
        'directory_creation': {
            'status': 'Not Started',
            'output': None
        },
        'save_explanation': {
            'status': 'Not Started',
            'output': None
        },
        'code_migration': {
            'status': 'Not Started',
            'output': None
        }
    }

# Display initial status message
with col0:
    st.header("Activity Log")
    st.info("Initializing...")

import migration_assistant
# Update status message after importing
with col0:
    st.info("Completed Initializing")

# Function to handle file input
def handle_file_input(inp_file_path):
    st.session_state['tasks']['code_explanation']['status'] = "In Progress"
    st.session_state['current_task'] = 'code_explanation'

    if os.path.exists(inp_file_path):
        st.success(f"CPP File exists: {inp_file_path}")
        st.session_state['status_message'] = "Code Analysis in Progress"
        st.session_state['input_file_path'] = inp_file_path
        with col0:
            st.info(st.session_state['status_message'])

        # Read the file and pass to the migration assistant
        code_exp = migration_assistant.analyze_cpp_files(inp_file_path)
        st.session_state['tasks']['code_explanation']['status'] = "Completed"
        st.session_state['tasks']['code_explanation']['output'] = code_exp.raw
        with col0:
            st.info(st.session_state['status_message'])

        # task_output = {"task": "Code Explanation", "task_success": True, "output": code_exp.raw}
    else:
        st.error(f"File does not exist: {inp_file_path}")
        st.session_state['status_message'] = "File does not exist"
        with col0:
            st.info(st.session_state['status_message'])
        st.session_state['tasks']['code_explanation']['status'] = "Failed"
        st.session_state['tasks']['code_explanation']['output'] = "File does not exist"
    with col0:
        st.info(f"Code Explanation Status: {st.session_state['tasks']['code_explanation']['status']}")
    return

# Function to create a new directory
def create_directory(directory):
    st.session_state['tasks']['directory_creation']['status'] = "In Progress"
    st.session_state['current_task'] = 'directory_creation'
    #check if directory already exists
    if os.path.exists(directory):
        st.success(f"Directory exists and is set as Target Directory: {directory}")
        st.session_state['tasks']['directory_creation']['status'] = "Completed"
        st.session_state['tasks']['directory_creation']['output'] = directory
        st.session_state['output_directory'] = directory
        with col0:
            st.info(f"Directory Setting Status: {st.session_state['tasks']['directory_creation']['status']}")

    else:
        # create directory if it doesn't exist
        try:
            os.makedirs(directory, exist_ok=True)
            st.success(f"Directory created: {directory}")
            st.session_state['tasks']['directory_creation']['status'] = "Completed"
            st.session_state['tasks']['directory_creation']['output'] = directory
            st.session_state['output_directory'] = directory
        except Exception as e:
            st.error(f"Error creating directory: {e}")
            st.session_state['tasks']['directory_creation']['status'] = "Failed"
            st.session_state['tasks']['directory_creation']['output'] = str(e)
        with col0:
            st.info(f"Directory Creation Status: {st.session_state['tasks']['directory_creation']['status']}")
    return

# Function to save code explanation to a markdown file
def save_code_explanation_to_md(directory, file_name, code_exp):
    st.session_state['tasks']['save_explanation']['status'] = "In Progress"
    st.session_state['current_task'] = 'save_explanation'
    md_file_path = os.path.join(directory, file_name + ".md")
    try:
        with open(md_file_path, "w") as md_file:
            md_file.write(code_exp)
        st.success(f"Code explanation saved to: {md_file_path}")
        st.session_state['tasks']['save_explanation']['status'] = "Completed"
        st.session_state['tasks']['save_explanation']['output'] = md_file_path
    except Exception as e:
        st.error(f"Error saving explanation: {e}")
        st.session_state['tasks']['save_explanation']['status'] = "Failed"
        st.session_state['tasks']['save_explanation']['output'] = ""
    with col0:
        st.info(f"Save Explanation Status: {st.session_state['tasks']['save_explanation']['status']}")
    return

# Function for impact analysis
def impact_analysis(input_text):
    st.write(f"Performing impact analysis on: {input_text}")
    # Add your impact analysis logic here

# Function for migrate_to_java
def migrate_to_java(java_filename,input_file_name):
    st.session_state['tasks']['code_migration']['status'] = "In Progress"
    st.session_state['current_task'] = 'code_migration'
    full_java_filename = os.path.join(st.session_state['output_directory'], java_filename)
    try:
        response = migration_assistant.cpp_to_java(full_java_filename, input_file_name)
        if response['success'] == True:
            st.success(f"Conversion to Java completed for: {input_file_name}")
            st.session_state['tasks']['code_migration']['status'] = "Completed"
            st.session_state['tasks']['code_migration']['output'] = java_filename
        else:
            st.error(f"Conversion to Java failed for: {input_file_name}")
            st.session_state['tasks']['code_migration']['status'] = "Failed"
            st.session_state['tasks']['code_migration']['output'] = ""
    except:
        st.error("Conversion to Java failed.")
        st.session_state['tasks']['code_migration']['status'] = "Failed"
        st.session_state['tasks']['code_migration']['output'] = ""
    with col0:
        st.info(f"Code Migration Status: {st.session_state['tasks']['code_migration']['status']}")
    return

# Left side - Directory and process management
with col1:
    st.header("Migration Steps")
    new_directory = st.text_input("1. Enter a new directory to save outputs:")
    if st.button("1.Set Target Directory"):
        create_directory(new_directory)
    #add button to select an input file
    # input_file = st.file_uploader("2. Select a C++ file:", type=["cpp", "h"])
    # if input_file:
    #     st.session_state['input_file_path'] = input_file

    if st.session_state['input_file_path'] is not None:
        directory_input = st.session_state['input_file_path']
    else:
        directory_input = st.text_input("Enter full c++ file path:")
    if st.button("2.Explain the c++ file"):
        handle_file_input(directory_input)

    new_file_code_explaination = st.text_input("Enter a new file name to save the explanation:")
    if st.button("3.Save explanation"):
        if st.session_state['tasks']['code_explanation']['status'] == "Completed":
            save_code_explanation_to_md(new_directory, new_file_code_explaination, st.session_state['tasks']['code_explanation']['output'])

    java_file_name = st.text_input("4.Enter the Java Filename:")
    if st.button("4.Convert to Java"):
        if (st.session_state['input_file_path'] is None) or (st.session_state['output_directory'] is None):
            with col0:
                st.info("ERROR: No input file selected for conversion to Java.")
        else:
            migrate_to_java(java_file_name, st.session_state['input_file_path'])

# Add vertical space between the sections
st.write("")
st.write("")

# Right side - Output & Chat
with col2:
    st.header("Output & Chat")
    #find number of tasks completed
    completed_tasks = sum(1 for task in st.session_state['tasks'].values() if task['status'] == 'Completed')
    st.text(f"Tasks Completed: {completed_tasks}/{len(st.session_state['tasks'])}")
    task_output_text = ""
    # Display current task status and output if available
    st.text(f"Current Task: {st.session_state['current_task']}")
    if completed_tasks >0 :
        if st.session_state['current_task'] == 'code_explanation':
            if 'code_explanation' in st.session_state['tasks'] and st.session_state['tasks']['code_explanation']['status'] == 'Completed':
                task_output_text = f"Output: {st.session_state['tasks']['code_explanation']['output']}"
            else:
                task_output_text = "No code explanation available yet."
        if st.session_state['current_task'] == 'code_migration':
            if 'code_migration' in st.session_state['tasks'] and st.session_state['tasks']['code_migration']['status'] == 'Completed':
                task_output_text = f"Output: {st.session_state['tasks']['code_migration']['output']}"
            else:
                task_output_text = "No Java file created yet."
    else:
        st.text("No Migration Task started yet. Please select a file to explain.")

    task_output = st.text_area(task_output_text, "", height=200)
    chat_input = st.text_area("")
    if st.button("Send Chat"):
        st.write(f"Chat message sent: {chat_input}")
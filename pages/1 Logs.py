import streamlit as st
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv() 

# Returns the path to the logs.json file
try:
    logs_file_path = os.getenv("ABSOLUTE_PATH_TO_SUBNET_REPO") + "/logging/logs.json"
except Exception as e:
    st.error("You did not set your environment variable")
    st.stop()

# Returns all logs from logs.json as a list of dictionaries
def get_logs():
    try:
        with open(logs_file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error reading logs: ({e})")
        st.info("Did you forget to set the environment variable? Cave is currently searching for " + logs_file_path)
        st.info("If you are sure you have set the environment variable, please check that the logging file exists at " + logs_file_path)
        st.info("If you are sure the file exists, please ensure a miner and validator are running")
        st.stop()

# Clears all logs by resetting logs.json to an empty array
def clear_logs():
    """Clear all logs by resetting logs.json to an empty array."""
    try:
        with open(logs_file_path, 'w') as f:
            json.dump([], f)
    except Exception as e:
        st.error(f"Error clearing log file ({e})")
        st.info("Did you forget to set the environment variable? Cave is currently searching for " + logs_file_path)
        st.info("If you are sure you have set the environment variable, please check that the logging file exists at " + logs_file_path)
        st.info("If you are sure the file exists, please ensure a miner and validator are running")
        st.stop()

# Returns the levelname of a log (without the ANSI color codes)
def get_log_levelname(log):
    return log['levelname'][9:-4]

# Returns the desired color of a log levelname
def get_log_color(log_levelname):
    if log_levelname == 'DEBUG':
        log_color = 'cyan'
    elif log_levelname == 'INFO':
        log_color = 'green'
    elif log_levelname == 'WARNING':
        log_color = 'yellow'
    elif log_levelname == 'ERROR' or log_levelname == 'CRITICAL':
        log_color = 'red'
    else:
        log_color = 'white'
    return log_color

# Outputs a log to the dashboard, displays JSON nicely if possible
def output_log(log):
    log_levelname = get_log_levelname(log)
    log_color = get_log_color(log_levelname)
    
    # Get active coroutines and format them
    active_coroutines = []
    if 'active_coroutines' in log:
        for coroutine in log['active_coroutines']:
            if coroutine == 'evaluation_task':
                active_coroutines.append(f"[{coroutine.upper()} loop #{log['eval_loop_num']}]")
            else:
                active_coroutines.append(f"[{coroutine.upper()}]")
    
    # Add coroutines to the output if any are active
    coroutine_text = " " + " ".join(active_coroutines) if active_coroutines else ""
    
    st.markdown(f"<span style='color: gray; font-style: italic;'>{log['timestamp']}</span> — <span style='color: {log_color};'>**{log_levelname}**</span> from `{log['pathname'] + ':' + str(log['lineno'])}`<span style='color: aqua;'>{coroutine_text}</span>", unsafe_allow_html=True)
    
    # Check if message is valid JSON, and output accordingly
    try:
        json_obj = json.loads(log['message'])
        st.json(json_obj)
    except (json.JSONDecodeError, TypeError):
        st.text(log['message'])
    
    # Spacing between logs
    st.text('\n')
    st.text('\n')

# Wide view
st.set_page_config(layout="wide")

# Create a container to store logs
log_container = st.empty()

# Initialize session state variables
if "logs" not in st.session_state:
    st.session_state.logs = []
if "files" not in st.session_state:
    st.session_state.files = []
if "file_selection" not in st.session_state:
    st.session_state.file_selection = None
if "levels" not in st.session_state:
    st.session_state.levels = []
if "level_selection" not in st.session_state:
    st.session_state.level_selection = None

# Display logs with log container
with log_container.container():
    # Get logs from logs.json
    st.session_state.logs = get_logs()

    # Get a list of all unique files and levels from the logs
    st.session_state.files = set([log['filename'] for log in st.session_state.logs])
    st.session_state.levels = set([get_log_levelname(log) for log in st.session_state.logs])
    st.session_state.coroutines = set([coroutine for log in st.session_state.logs for coroutine in log['active_coroutines']])
    st.session_state.loop_nums = set([log['eval_loop_num'] for log in st.session_state.logs if log['eval_loop_num'] != 0])

    # Sidebar for filters and clearing logs
    with st.sidebar:
        st.session_state.file_selection = st.selectbox("Filter by file", st.session_state.files, index=None)
        st.session_state.level_selection = st.selectbox("Filter by level", st.session_state.levels, index=None)
        st.session_state.coroutine_selection = st.multiselect("Filter by coroutine", st.session_state.coroutines)
        st.session_state.loop_num_selection = st.selectbox("Filter by evaluation loop number", st.session_state.loop_nums, index=None)
        if st.button("Clear existing logs", type="primary"):
            clear_logs()
            st.rerun()

    # Title and refresh text
    st.subheader("Subnet Logs")
    st.text("Press R to refresh to see latest logs (working on a fix for this)")

    # Display the selected filters
    st.divider()
    if st.session_state.file_selection is not None:
        st.markdown(f"Displaying logs from `{st.session_state.file_selection}`")
    if st.session_state.level_selection is not None:
        log_color = get_log_color(st.session_state.level_selection)
        st.markdown(f"Displaying logs with level <span style='color: {log_color};'>**{st.session_state.level_selection}**</span>", unsafe_allow_html=True)
    if st.session_state.coroutine_selection != []:
        st.markdown(f"Displaying logs that occured during coroutine(s) <span style='color: aqua;'>**{' or '.join(['[' + c.upper() + ']' for c in st.session_state.coroutine_selection])}**</span>", unsafe_allow_html=True)
    if st.session_state.loop_num_selection is not None:
        st.markdown(f"Displaying logs that occured during loop number <span style='color: aquamarine;'>**{st.session_state.loop_num_selection}**</span>", unsafe_allow_html=True)
    st.divider()

    # Display the logs that match the selected filters
    num_logs_ouputted = 0
    for log in reversed(st.session_state.logs):
        if (st.session_state.file_selection is None or log['filename'] in st.session_state.file_selection) and (st.session_state.level_selection is None or get_log_levelname(log) in st.session_state.level_selection) and (st.session_state.coroutine_selection == [] or any(coroutine in log['active_coroutines'] for coroutine in st.session_state.coroutine_selection)) and (st.session_state.loop_num_selection is None or (log['eval_loop_num'] == st.session_state.loop_num_selection and 'evaluation_task' in log['active_coroutines'])):
            output_log(log)
            num_logs_ouputted += 1
    
    # Output the number of logs that match the selected filters
    st.divider()
    st.text(f"Displayed {num_logs_ouputted} logs out of {len(st.session_state.logs)} total logs that match the selected filters (if applicable)")
    if num_logs_ouputted == 0:
        st.info("No logs appeared. Please update your filters (or you may have no logs)")

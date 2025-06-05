import streamlit as st
from datetime import datetime
from typing import Optional, List
import sqlite3
from dotenv import load_dotenv
import os
from models import RegressionResponse

# Load environment variables
load_dotenv() 

# Get the absolute path to the database
try:
    db_path = os.getenv("ABSOLUTE_PATH_TO_SUBNET_REPO") + "/validator.db"
except Exception as e:
    st.error("You did not set your environment variable")
    st.stop()

st.set_page_config(layout="wide")

def get_regression_responses(db_path: str = db_path) -> List[RegressionResponse]:
    """
    Read all regression responses from the database and return them as a list of RegressionResponse objects.
    
    Args:
        db_path (str): Path to the SQLite database file
        
    Returns:
        List[RegressionResponse]: List of RegressionResponse objects
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT r.response_id, r.challenge_id, r.miner_hotkey, r.node_id, 
                       r.processing_time, r.received_at, r.completed_at, 
                       r.evaluated, r.score, r.evaluated_at, rr.response_patch
                FROM responses r
                JOIN regression_responses rr ON r.response_id = rr.response_id
                JOIN challenges c ON r.challenge_id = c.challenge_id
                WHERE c.type = 'regression'
            """)
            return [RegressionResponse.from_db_row(row) for row in cursor.fetchall()]
    except Exception as e:
        st.error(f"Error reading from validator.db ({e})")
        st.info("Did you forget to set your environment variable? Cave is currently searching for " + db_path)
        st.info("If you are sure you have set the environment variable, please check that the database file exists at " + db_path)
        st.info("If you are sure the file exists, please ensure a miner and validator are running")
        st.stop()

# Get and process responses
responses = get_regression_responses()

for response in responses:
    response.processing_time = str(response.completed_at - response.received_at).split('.')[0]

responses_dict = [response.to_dict() for response in responses]

if len(responses) == 0:
    st.info("No regression responses found in " + db_path + ". Please ensure a miner and validator are running.")
    st.stop()

# Display responses table
st.subheader('Regression Responses')
responses_df = st.dataframe(
    responses_dict,
    column_order=['response_id', 'challenge_id', 'miner_hotkey', 'node_id', 'processing_time', 
                 'received_at', 'completed_at', 'evaluated', 'score', 'evaluated_at', 'response_patch'],
    on_select="rerun",
    selection_mode="single-row",
    hide_index=True
)

try:
    row_num = responses_df['selection']['rows'][0]
    selected_response = responses_dict[row_num]
    st.subheader('Response patch')
    st.code(selected_response['response_patch'], language='diff')
except:
    st.write("Select a response to see the patch")
    pass 
import streamlit as st
from datetime import datetime
from typing import Optional, List
import sqlite3
import json
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv() 

# Get the absolute path to the database
try:
    db_path = os.getenv("ABSOLUTE_PATH_TO_SUBNET_REPO") + "/validator.db"
except Exception as e:
    st.error("You did not set your environment variable")
    st.stop()

st.set_page_config(layout="wide")

class CodegenChallenge:
    def __init__(
        self,
        challenge_id: str,
        created_at: datetime,
        question_text: str,
        relevant_filepair_1_name: str,
        relevant_filepair_2_name: str,
        dynamic_checklist: List[str]
    ):
        self.challenge_id = challenge_id
        self.created_at = created_at
        self.question_text = question_text
        self.relevant_filepair_1_name = relevant_filepair_1_name
        self.relevant_filepair_2_name = relevant_filepair_2_name
        self.dynamic_checklist = dynamic_checklist

    def to_dict(self) -> dict:
        """Convert the object to a dictionary for database operations"""
        return {
            'challenge_id': self.challenge_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'question_text': self.question_text,
            'relevant_filepair_1_name': self.relevant_filepair_1_name,
            'relevant_filepair_2_name': self.relevant_filepair_2_name,
            'dynamic_checklist': json.dumps(self.dynamic_checklist)
        }

    @classmethod
    def from_db_row(cls, row: tuple) -> 'CodegenChallenge':
        """Create a CodegenChallenge instance from a database row"""
        return cls(
            challenge_id=row[0],
            created_at=datetime.fromisoformat(row[1]) if row[1] else None,
            question_text=row[2],
            relevant_filepair_1_name=row[3],
            relevant_filepair_2_name=row[4],
            dynamic_checklist=json.loads(row[5])
        )

def get_all_codegen_challenges(db_path: str = db_path) -> List[CodegenChallenge]:
    """
    Read all codegen challenges from the database and return them as a list of CodegenChallenge objects.
    
    Args:
        db_path (str): Path to the SQLite database file
        
    Returns:
        List[CodegenChallenge]: List of CodegenChallenge objects
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM codegen_challenges")
            return [CodegenChallenge.from_db_row(row) for row in cursor.fetchall()]
    except Exception as e:
        st.error(f"Error reading from validator.db ({e})")
        st.info("Did you forget to set the environment variable? Cave is currently searching for " + db_path)
        st.info("If you are sure you have set the environment variable, please check that the database file exists at " + db_path)
        st.info("If you are sure the file exists, please ensure a miner and validator are running")
        st.stop()

# Get all codegen challenges
challenges = get_all_codegen_challenges()
challenges_dict = [challenge.to_dict() for challenge in challenges]

if len(challenges) == 0:
    st.info("No codegen challenges found in " + db_path + ". Please ensure a miner and validator are running.")
    st.stop()

# Display challenges table
st.subheader('Codegen Challenges table')
challenges_df = st.dataframe(
    challenges_dict,
    column_order=['challenge_id', 'created_at', 'question_text', 'relevant_filepair_1_name', 
                 'relevant_filepair_2_name', 'dynamic_checklist'],
    on_select="rerun",
    selection_mode="single-row",
    hide_index=True
)

# Display challenge details when selected
try:
    row_num = challenges_df['selection']['rows'][0]
    selected_challenge = challenges[row_num]
    
    st.subheader(f'Challenge {selected_challenge.challenge_id}')
    st.write('**Question:**')
    st.write(selected_challenge.question_text)
    
    st.write('**Relevant Files:**')
    st.write(f"1. `{selected_challenge.relevant_filepair_1_name}`")
    st.write(f"2. `{selected_challenge.relevant_filepair_2_name}`")
    
    st.write('**Dynamic Checklist:**')
    for item in selected_challenge.dynamic_checklist:
        st.checkbox(f"{item}")
except:
    st.write("Select a challenge from the table to see its details")
    pass

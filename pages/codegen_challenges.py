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
        problem_statement: str,
        dynamic_checklist: List[str],
        repository_url: str,
        commit_hash: Optional[str],
        context_file_paths: List[str]
    ):
        self.challenge_id = challenge_id
        self.created_at = created_at
        self.problem_statement = problem_statement
        self.dynamic_checklist = dynamic_checklist
        self.repository_url = repository_url
        self.commit_hash = commit_hash
        self.context_file_paths = context_file_paths

    def to_dict(self) -> dict:
        """Convert the object to a dictionary for database operations"""
        return {
            'challenge_id': self.challenge_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'problem_statement': self.problem_statement,
            'dynamic_checklist': json.dumps(self.dynamic_checklist),
            'repository_url': self.repository_url,
            'commit_hash': self.commit_hash,
            'context_file_paths': json.dumps(self.context_file_paths)
        }

    @classmethod
    def from_db_row(cls, row: tuple) -> 'CodegenChallenge':
        """Create a CodegenChallenge instance from a database row"""
        return cls(
            challenge_id=row[0],
            created_at=datetime.fromisoformat(row[1]) if row[1] else None,
            problem_statement=row[2],
            dynamic_checklist=json.loads(row[3]),
            repository_url=row[4],
            commit_hash=row[5],
            context_file_paths=json.loads(row[6])
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
            cursor.execute("""
                SELECT cc.challenge_id, c.created_at, cc.problem_statement, 
                       cc.dynamic_checklist, cc.repository_url, cc.commit_hash, cc.context_file_paths
                FROM codegen_challenges cc
                JOIN challenges c ON cc.challenge_id = c.challenge_id
                WHERE c.type = 'codegen'
            """)
            return [CodegenChallenge.from_db_row(row) for row in cursor.fetchall()]
    except Exception as e:
        st.error(f"Error reading from validator.db ({e})")
        st.info("Did you forget to set your environment variable? Cave is currently searching for " + db_path)
        st.info("If you are sure you have set the environment variable, please check that the database file exists at " + db_path)
        st.info("If you are sure the file exists, please ensure a miner and validator are running")
        st.stop()

# Get all codegen challenges
challenges = get_all_codegen_challenges()
challenges_dict = [challenge.to_dict() for challenge in challenges]

if len(challenges) == 0:
    st.info("No codegen challenges found in " + db_path + ". Please ensure a miner and validator are running. It may be the case that everything is fine, but your codegen_challenges table is empty.")
    st.stop()

# Display challenges table
st.subheader('Codegen Challenges table')
challenges_df = st.dataframe(
    challenges_dict,
    column_order=['challenge_id', 'created_at', 'problem_statement', 'repository_url', 
                 'commit_hash', 'context_file_paths', 'dynamic_checklist'],
    on_select="rerun",
    selection_mode="single-row",
    hide_index=True
)

# Display challenge details when selected
try:
    row_num = challenges_df['selection']['rows'][0]
    selected_challenge = challenges[row_num]
    
    st.subheader(f'Challenge {selected_challenge.challenge_id}')
    
    # Repository Information
    st.write('**Repository Information:**')
    st.write(f"Repository: `{selected_challenge.repository_url}`")
    if selected_challenge.commit_hash:
        st.write(f"Commit: `{selected_challenge.commit_hash}`")
    
    # Problem Statement
    st.write('**Problem Statement:**')
    st.write(selected_challenge.problem_statement)
    
    # Context Files
    st.write('**Context Files:**')
    for i, file_path in enumerate(selected_challenge.context_file_paths, 1):
        st.write(f"{i}. `{file_path}`")
    
    # Dynamic Checklist
    st.write('**Dynamic Checklist:**')
    for item in selected_challenge.dynamic_checklist:
        st.checkbox(f"{item}")
except:
    st.write("Select a challenge from the table to see its details")
    pass

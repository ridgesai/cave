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

class RegressionChallenge:
    def __init__(
        self,
        challenge_id: str,
        created_at: datetime,
        problem_statement: str,
        repository_url: str,
        commit_hash: Optional[str],
        context_file_paths: List[str]
    ):
        self.challenge_id = challenge_id
        self.created_at = created_at
        self.problem_statement = problem_statement
        self.repository_url = repository_url
        self.commit_hash = commit_hash
        self.context_file_paths = context_file_paths

    def to_dict(self) -> dict:
        """Convert the object to a dictionary for database operations"""
        return {
            'challenge_id': self.challenge_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'problem_statement': self.problem_statement,
            'repository_url': self.repository_url,
            'commit_hash': self.commit_hash,
            'context_file_paths': json.dumps(self.context_file_paths)
        }

    @classmethod
    def from_db_row(cls, row: tuple) -> 'RegressionChallenge':
        """Create a RegressionChallenge instance from a database row"""
        return cls(
            challenge_id=row[0],
            created_at=datetime.fromisoformat(row[1]) if row[1] else None,
            problem_statement=row[2],
            repository_url=row[3],
            commit_hash=row[4],
            context_file_paths=json.loads(row[5])
        )

def get_all_regression_challenges(db_path: str = db_path) -> List[RegressionChallenge]:
    """
    Read all regression challenges from the database and return them as a list of RegressionChallenge objects.
    
    Args:
        db_path (str): Path to the SQLite database file
        
    Returns:
        List[RegressionChallenge]: List of RegressionChallenge objects
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT rc.challenge_id, c.created_at, rc.problem_statement, 
                       rc.repository_url, rc.commit_hash, rc.context_file_paths
                FROM regression_challenges rc
                JOIN challenges c ON rc.challenge_id = c.challenge_id
                WHERE c.type = 'regression'
            """)
            return [RegressionChallenge.from_db_row(row) for row in cursor.fetchall()]
    except Exception as e:
        st.error(f"Error reading from validator.db ({e})")
        st.info("Did you forget to set your environment variable? Cave is currently searching for " + db_path)
        st.info("If you are sure you have set the environment variable, please check that the database file exists at " + db_path)
        st.info("If you are sure the file exists, please ensure a miner and validator are running")
        st.stop()

# Get all regression challenges
challenges = get_all_regression_challenges()
challenges_dict = [challenge.to_dict() for challenge in challenges]

if len(challenges) == 0:
    st.info("No regression challenges found in " + db_path + ". Please ensure a miner and validator are running. It may be the case that everything is fine, but your regression_challenges table is empty.")
    st.stop()

# Display challenges table
st.subheader('Regression Challenges table')
challenges_df = st.dataframe(
    challenges_dict,
    column_order=['challenge_id', 'created_at', 'problem_statement', 'repository_url', 
                 'commit_hash', 'context_file_paths'],
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
except:
    st.write("Select a challenge from the table to see its details")
    pass 
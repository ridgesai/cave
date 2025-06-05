import streamlit as st
from datetime import datetime
from typing import Optional, List
import sqlite3
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

class Response:
    def __init__(
        self,
        response_id: Optional[int] = None,  # Optional because it's auto-incrementing
        challenge_id: str = None,
        type: str = None,
        miner_hotkey: str = None,
        node_id: Optional[int] = None,
        processing_time: Optional[float] = None,
        received_at: datetime = None,
        completed_at: Optional[datetime] = None,
        evaluated: bool = False,
        score: Optional[float] = None,
        evaluated_at: Optional[datetime] = None,
        response_patch: Optional[str] = None
    ):
        self.response_id = response_id
        self.challenge_id = challenge_id
        self.type = type
        self.miner_hotkey = miner_hotkey
        self.node_id = node_id
        self.processing_time = processing_time
        self.received_at = received_at or datetime.now()
        self.completed_at = completed_at
        self.evaluated = evaluated
        self.score = score
        self.evaluated_at = evaluated_at
        self.response_patch = response_patch

    def to_dict(self) -> dict:
        """Convert the object to a dictionary for database operations"""
        return {
            'response_id': self.response_id,
            'challenge_id': self.challenge_id,
            'type': self.type,
            'miner_hotkey': self.miner_hotkey,
            'node_id': self.node_id,
            'processing_time': self.processing_time,
            'received_at': self.received_at.isoformat() if self.received_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'evaluated': self.evaluated,
            'score': self.score,
            'evaluated_at': self.evaluated_at.isoformat() if self.evaluated_at else None,
            'response_patch': self.response_patch
        }

    @classmethod
    def from_db_row(cls, row: tuple) -> 'Response':
        """Create a Response instance from a database row"""
        return cls(
            response_id=row[0],
            challenge_id=row[1],
            type=row[2],
            miner_hotkey=row[3],
            node_id=row[4],
            processing_time=float(row[5]) if row[5] is not None else None,
            received_at=datetime.fromisoformat(row[6]) if row[6] else None,
            completed_at=datetime.fromisoformat(row[7]) if row[7] else None,
            evaluated=bool(row[8]),
            score=float(row[9]) if row[9] is not None else None,
            evaluated_at=datetime.fromisoformat(row[10]) if row[10] else None,
            response_patch=row[11]
        )

def get_pending_responses(db_path: str = db_path) -> List[Response]:
    """
    Read all pending (unevaluated) responses from the database and return them as a list of Response objects.
    
    Args:
        db_path (str): Path to the SQLite database file
        
    Returns:
        List[Response]: List of Response objects
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT r.response_id, r.challenge_id, c.type, r.miner_hotkey, 
                       r.node_id, r.processing_time, r.received_at, r.completed_at, 
                       r.evaluated, r.score, r.evaluated_at, r.response_patch
                FROM responses r
                JOIN challenges c ON r.challenge_id = c.challenge_id
                WHERE r.evaluated = 0
                ORDER BY r.received_at DESC
            """)
            return [Response.from_db_row(row) for row in cursor.fetchall()]
    except Exception as e:
        st.error(f"Error reading from validator.db ({e})")
        st.info("Did you forget to set your environment variable? Cave is currently searching for " + db_path)
        st.info("If you are sure you have set the environment variable, please check that the database file exists at " + db_path)
        st.info("If you are sure the file exists, please ensure a miner and validator are running")
        st.stop()

# Get and process pending responses
responses = get_pending_responses()

for response in responses:
    response.processing_time = str(response.completed_at - response.received_at).split('.')[0]

responses_dict = [response.to_dict() for response in responses]

if len(responses) == 0:
    st.info("No pending responses found in " + db_path + ". All responses have been evaluated.")
    st.stop()

# Display pending responses table
st.subheader('Pending Responses')
st.write(f"Found {len(responses)} pending responses")

# Add filters in the sidebar
with st.sidebar:
    st.subheader("Filters")
    
    # Filter by challenge type
    types = sorted(list(set(r['type'] for r in responses_dict)))
    selected_type = st.selectbox("Challenge Type", ["All"] + types)
    
    # Filter by node
    nodes = sorted(list(set(r['node_id'] for r in responses_dict if r['node_id'] is not None)))
    selected_node = st.selectbox("Node ID", ["All"] + [str(n) for n in nodes])
    
    # Filter by miner
    miners = sorted(list(set(r['miner_hotkey'] for r in responses_dict)))
    selected_miner = st.selectbox("Miner Hotkey", ["All"] + miners)

# Apply filters
filtered_responses = responses_dict
if selected_type != "All":
    filtered_responses = [r for r in filtered_responses if r['type'] == selected_type]
if selected_node != "All":
    filtered_responses = [r for r in filtered_responses if str(r['node_id']) == selected_node]
if selected_miner != "All":
    filtered_responses = [r for r in filtered_responses if r['miner_hotkey'] == selected_miner]

# Display filtered responses
responses_df = st.dataframe(
    filtered_responses,
    column_order=['response_id', 'challenge_id', 'type', 'miner_hotkey', 'node_id', 'processing_time', 
                 'received_at', 'completed_at', 'response_patch'],
    on_select="rerun",
    selection_mode="single-row",
    hide_index=True
)

# Display response details when selected
try:
    row_num = responses_df['selection']['rows'][0]
    selected_response = filtered_responses[row_num]
    
    st.subheader('Response Details')
    st.write(f"**Challenge Type:** {selected_response['type']}")
    st.write(f"**Miner:** `{selected_response['miner_hotkey']}`")
    st.write(f"**Node ID:** {selected_response['node_id']}")
    st.write(f"**Processing Time:** {selected_response['processing_time']}")
    st.write(f"**Received At:** {selected_response['received_at']}")
    st.write(f"**Completed At:** {selected_response['completed_at']}")
    
    st.subheader('Response Patch')
    st.code(selected_response['response_patch'], language='diff')
except:
    st.write("Select a response to see its details")
    pass 
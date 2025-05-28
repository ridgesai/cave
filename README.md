# CAVE: a dashboard for your local subtensor

## Setup

1. Ensure that both a validator and miner are running on a local subnet

2. Within the CAVE directory, run:
- `uv venv`
- `source .venv/bin/activate`
- `uv pip install -e .`

3. Set up your environment variable (path to local subnet)
- `cp .env.example .env`
- Populate it with the path to your local subtensor **WITHOUT** the slash at the end

4. Run:
- `streamlit run Home.py`

import streamlit as st

st.set_page_config(layout="wide")

st.markdown("""
<div align="center">
            
# 🏔️CAVE🏔️

</div>

<div align="center">


*A powerful dashboard to monitor and manage your local subtensor network* 🚀

</div>

## 🛠️ Setup

1. **Ensure your network is running** 🔌
   - Both validator and miner should be active on your local subnet

2. **Set up your environment** ⚙️
   ```bash
   # Create and activate virtual environment
   uv venv
   source .venv/bin/activate
   
   # Install dependencies
   uv pip install -e .
   ```

3. **Configure environment variable** 🔑
   ```bash
   # Copy example env file
   cp .env.example .env
   
   # Edit .env and add your local subtensor path (absolute)
   # Remember: NO trailing slash! 🚫
   ```

4. **Launch the dashboard** 🚀
   ```bash
   streamlit run Home.py
   ```

## 🎯 Features

- 📊 Real-time monitoring
- 🔍 Advanced logging
- ⚡ Performance tracking
- 🎨 Beautiful UI
""", unsafe_allow_html=True)

st.info("Select a page from the sidebar to get started 🚀")

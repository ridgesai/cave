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

## 📝 Logging Guide

### 🎯 Quick Start
1. **Check your setup** 🔍
   - Ensure your subnet has our pre-configured `logging` folder
   - Verify `logging_utils.py` exists in the folder

2. **Start logging** ⚡
   ```python
   from logging.logging_utils import get_logger
   
   # Initialize logger with your module name
   logger = get_logger(__name__)
   
   # Log away! 🚀
   logger.debug("Detailed information for debugging")
   logger.info("General information about program execution")
   logger.warning("Warning messages for potentially problematic situations")
   logger.error("Error messages for serious problems")
   logger.critical("Critical messages for fatal errors")
   ```

### 🎨 Log Levels
| Level | Color | When to Use |
|-------|-------|-------------|
| DEBUG | <span style="color: cyan">Cyan</span> | Detailed information for debugging |
| INFO | <span style="color: green">Green</span> | General information about program execution |
| WARNING | <span style="color: yellow">Yellow</span> | Potentially problematic situations |
| ERROR | <span style="color: red">Red</span> | Serious problems that need attention |
| CRITICAL | <span style="color: red">Red</span> | Fatal errors that may lead to program termination |

### 📊 JSON Logging
  ```python
  # Good: Clean JSON logging
  logger.info(json.dumps({"status": "success", "data": {...}}))
  
  # Bad: Mixed content
  logger.info(f"Status: {json.dumps(data)}")  # Don't do this!
  ```

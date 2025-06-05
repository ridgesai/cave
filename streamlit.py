import streamlit as st

cave_page = st.Page("pages/cave.py", title="Cave")
logs_page = st.Page("pages/logs.py", title="Logging")
availability_check_page = st.Page("pages/availability_checks.py", title="Availability Checks")
challenge_assignments_page = st.Page("pages/challenge_assignments.py", title="Challenge Assignments")
codegen_challenges_page = st.Page("pages/codegen_challenges.py", title="Codegen Challenges")
regression_challenges_page = st.Page("pages/regression_challenges.py", title="Regression Challenges")
codegen_responses_page = st.Page("pages/codegen_responses.py", title="Codegen Responses")
regression_responses_page = st.Page("pages/regression_responses.py", title="Regression Responses")

pg = st.navigation([cave_page, logs_page, availability_check_page, challenge_assignments_page, codegen_challenges_page, regression_challenges_page, codegen_responses_page, regression_responses_page])
pg.run()

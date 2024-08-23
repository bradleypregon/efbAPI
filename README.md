# SimBriefCleaner
Python data cleaner and API for SimBrief and efbUI

This app takes a JSON API response from SimBrief and strips it to what /i/ need for my efbUI.
It also uses FastAPI and Uvicorn to create a server which will send the "cleaned" data to my efbUI app.

Minimal path to awesome:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd src
python3 api.py
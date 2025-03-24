""" 
OVERVIEW: this code creates a visual tech (technology) tree for techs learned in robotics 
and organizes them based on their dependent techs. this code will:

setup python ENV:
python3 -m venv myenv
source myenv/bin/activate 
pip install graphviz gspread gspread-formatting google-auth google-api-python-client google-auth-httplib2 google-auth-oauthlib dash plotly networkx numpy

run python dash app
python3 ./tech_tree_v2.py <path_to_google_api_credentials>.json <google_sheet_id> userAction

SHARING: the google sheet and the folder in which it lives must be shared with the API email and given 'edit access'
"""

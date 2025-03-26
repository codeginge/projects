""" 
OVERVIEW: this code creates a visual tech (technology) tree for techs learned in robotics 
and organizes them based on their dependent techs. this code will:

setup python ENV:
python3 -m venv myenv
source myenv/bin/activate 
pip install graphviz gspread gspread-formatting google-auth google-api-python-client google-auth-httplib2 google-auth-oauthlib dash plotly networkx numpy psycopg2-binary

run python dash app
python3 ./tech_tree_v2.py <path_to_google_api_credentials>.json <google_sheet_id> userAction

SHARING: the google sheet and the folder in which it lives must be shared with the API email and given 'edit access'
"""

### IMPORTS ###
import psycopg2, json


### FUNCTIONS ###
def psql_connect(psql_db, psql_usr, psql_pswd, psql_hst):
    """
    psql_db   : string
    psql_usr  : string
    psql_pswd : string
    psql_hst  : string
    """
    # attempt connection
    conn = psycopg2.connect(dbname=psql_db, user=psql_usr, password=psql_pswd, host=psql_hst)

    return(conn)


def psql_pull():
    # attempt pull
    
    return(json_data)


def psql_push():
    push_status = false
    #attempt push
    
    return(push_status)

psql_connect("techdb","techuser","tech","localhost")
""" 
OVERVIEW: this code creates a visual tech (technology) tree for techs learned in robotics 
and organizes them based on their dependent techs. this code will:

1. opens a google sheet with this data structure:
|--name--|--type--|--sub_type--|--difficulty--|--letter--|--num--|--id--|--depends--|--notes--|

2. creates a json data set from the goolge sheet with this data stucture:

"robotics/other/techs.json"
[
	{
		"name":"Light - LED", 
		"type":"actuators", 
        "sub_type":"light", 
		"difficulty":1,
		"id":"a1_01", 
		"depends":["c1_01","c1_02","c1_03"],
		"notes":"Basic light-emitting diode for signaling or lighting in various colors."
	},
	{
		"name":"Barometric Pressure and Temperature - BMP280", 
		"type":"sensors", 
        "subtype":"temp", 
		"difficulty":2,
		"id":"s2_02", 
		"dependent_on":["s1","s1_10","s1_11","s1_05"],
		"notes":"Improved version of BMP180 with temperature readings."
	}
]

3. sorts the technologies by type and then by dependencies. 

4. creates a tech tree visual from the dependency sorted list and outputs it as a .png file in ../other


Example CMD:
python3 -m venv myenv && source myenv/bin/activate && pip install graphviz && pip show graphviz && pip install gspread google-auth
python3 ./tech_tree.py ../../../../Downloads/circuits_tech_tree-techDataSheet.csv ../other/techs.json
"""
import gspread
from google.oauth2.service_account import Credentials
import csv
import json
import argparse
from graphviz import Digraph


# Set up argument parsing to accept both CSV file path and JSON output file name
parser = argparse.ArgumentParser(description="Convert Arduino Tech Tree CSV to JSON format.")
parser.add_argument("google_creds", help="path to the google json api key")
parser.add_argument("sheet_id", help="google sheet id")
parser.add_argument("sheet_name", help="google sheet name")
#parser.add_argument("output_filename", help="output file name")

args = parser.parse_args()
# Accessing the arguments
google_creds = args.google_creds
sheet_id = args.sheet_id
sheet_name = args.sheet_name
#output_filename = args.output_filename

# pull current sheet from google
def access_google_sheet(json_key_path, sheet_id, sheet_name):
    """
    Fetches and returns Google Sheet data as a structured JSON list.
    
    :param json_key_path: Path to Google service account JSON key file.
    :param sheet_id: The ID of the Google Sheet (from the URL).
    :param sheet_name: The name of the sheet/tab inside the spreadsheet.
    :return: List of dictionaries representing sheet data in the desired format.
    """
    # Define scope
    scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

    # Authenticate using service account file
    creds = Credentials.from_service_account_file(json_key_path, scopes=scopes)
    client = gspread.authorize(creds)

    # Open the Google Sheet by ID and select the sheet
    worksheet = client.open_by_key(sheet_id).worksheet(sheet_name)

    # Get all data as a list of lists
    raw_data = worksheet.get_all_values()

    # Extract headers from the first row
    headers = raw_data[1]

    # Print the headers for debugging
    print("Headers in the sheet:", headers)

    # Convert sheet data into a list of dictionaries
    json_data = []
    for row in raw_data[2:]:  # Skip header row
        entry = dict(zip(headers, row))

        # Convert 'difficulty' to an integer based on the prefix number
        if "difficulty" in entry:
            difficulty_value = entry["difficulty"]
            # Extract the number from the difficulty string
            if "_" in difficulty_value:
                entry["difficulty"] = int(difficulty_value.split("_")[0])  # Get the number part
            else:
                entry["difficulty"] = None  # In case the difficulty is not in the expected format
        else:
            entry["difficulty"] = None  # Handle missing difficulty gracefully

        # Convert 'depends' to a list (split by commas and strip spaces)
        if "depends" in entry:
            entry["depends"] = [dep.strip() for dep in entry["depends"].split(" ") if dep.strip()]
        else:
            entry["depends"] = []  # Handle missing depends gracefully

        # Set the output JSON structure
        formatted_entry = {
            "name": entry.get("name", ""),
            "type": entry.get("type", ""),
            "sub_type": entry.get("sub_type", ""),
            "difficulty": entry.get("difficulty", None),
            "id": entry.get("id", ""),
            "depends": entry.get("depends", []),
            "notes": entry.get("notes", "")
        }

        # Add formatted entry to the JSON data list
        json_data.append(formatted_entry)
    # DEBUG print(json.dumps(json_data, indent=4))
    return json_data


def create_flowchart_depends(data, output_file):
    # Initialize the graph
    dot = Digraph(format="png")
    dot.attr(rankdir="TB")  # Top-to-bottom layout
    dot.attr("node", shape="box", style="filled", fontname="Arial")
    dot.attr(splines="false")  # Disable curved edges, force straight lines
    dot.attr(ranksep="0.6", nodesep="0.3")  # Keep nodes closer without overlapping

    # Define colors for each type
    type_colors = {
        "actuators": "lightgreen",
        "sensors": "lightblue",
        "programming": "lightyellow",
        "wiring": "lightseagreen",
        "circuit_knowledge": "lightpink",
    }

    # Group nodes by type
    type_groups = {}
    for item in data:
        type_groups.setdefault(item["type"], []).append(item)

    # Add clusters for each type with a bold, larger title
    for type_name, items in type_groups.items():
        with dot.subgraph(name=f'cluster_{type_name}') as sub:
            sub.attr(label=f'<<B><FONT POINT-SIZE="50">{type_name}</FONT></B>>', fontname="Arial", style="dashed")
            for item in items:
                type_color = type_colors.get(item["type"], "lightgray")  # Default to lightgray
                sub.node(item["id"], f'{item["name"]}\n({item["id"]})', fillcolor=type_color, width="1", height="0.4")

    # Ensure dependent nodes appear **below** their dependencies
    for item in data:
        for dependency in item["depends"]:
            dot.edge(dependency, item["id"], constraint="true", minlen="1")  # Forces vertical placement

    # Save and render the graph
    dot.render(f'../other/{output_file}', cleanup=True)
    print(f"Flowchart saved to {output_file}.png")



# Create the flowchart
create_flowchart_depends(access_google_sheet(google_creds, sheet_id, sheet_name),sheet_name)

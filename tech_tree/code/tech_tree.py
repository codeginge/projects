""" 
OVERVIEW: this code creates a visual tech (technology) tree for techs learned in robotics 
and organizes them based on their dependent techs. this code will:

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


def access_google_sheet(json_key_path, sheet_id, sheet_name):
    """
    Fetches and returns Google Sheet data as a structured JSON list.
    If an entry lacks an ID, it generates one that does not conflict with existing IDs.
    
    :param json_key_path: Path to Google service account JSON key file.
    :param sheet_id: The ID of the Google Sheet (from the URL).
    :param sheet_name: The name of the sheet/tab inside the spreadsheet.
    :return: List of dictionaries representing sheet data in the desired format.
    """

    creds = Credentials.from_service_account_file(json_key_path, scopes=["https://www.googleapis.com/auth/spreadsheets"])
    client = gspread.authorize(creds)

    # Open the Google Sheet and select the worksheet
    worksheet = client.open_by_key(sheet_id).worksheet(sheet_name)

    # Get all data as a list of lists
    raw_data = worksheet.get_all_values()

    # Extract headers from the first row
    headers = raw_data[1]  # Assuming the second row contains headers
    id_col_index = headers.index("id") + 1  # Find index of the "id" column (1-based for Google Sheets)
    core_col_index = headers.index("core") + 1  # Find index of the "core" column (1-based)

    # Get existing IDs to prevent conflicts
    existing_ids = set(row[id_col_index - 1] for row in raw_data[2:] if row[id_col_index - 1])  # Get non-empty IDs

    # Convert sheet data into a list of dictionaries
    json_data = []
    type_counters = {}  # Track sequence numbers for each type
    updates = []  # Store batch updates (cell range, value)

    for i, row in enumerate(raw_data[2:], start=3):  # Skip header row (1-based index)
        entry = dict(zip(headers, row))

        # Convert 'dependency' to a list (split by spaces and strip spaces)
        entry["dependency"] = [dep.strip() for dep in entry.get("dependency", "").split(" ") if dep.strip()]

        # Check if 'core' is empty or 'x', set it accordingly
        core_value = row[core_col_index - 1].strip()  # Get the value from the "core" column
        entry["core"] = True if core_value.lower() == "x" else False

        # Generate ID if missing
        if not entry.get("id"):
            type_prefix = entry["type"][:3].upper()  # First 3 letters of type
            num = type_counters.get(type_prefix, 0) + 1
            new_id = f"{type_prefix}{num:03d}"

            # Ensure ID is unique
            while new_id in existing_ids:
                num += 1
                new_id = f"{type_prefix}{num:03d}"

            # Assign final unique ID
            entry["id"] = new_id
            existing_ids.add(new_id)  # Add to existing IDs to avoid future conflicts
            type_counters[type_prefix] = num  # Update counter for this type

            # Store update for batch processing
            cell_range = f"{chr(64 + id_col_index)}{i}"  # Convert to A1 notation (e.g., "C4")
            updates.append({"range": cell_range, "values": [[new_id]]})

        # Set the output JSON structure
        formatted_entry = {
            "name": entry.get("name", ""),
            "type": entry.get("type", ""),
            "sub_type": entry.get("sub_type", ""),
            "id": entry["id"],
            "dependency": entry.get("dependency", []),
            "notes": entry.get("notes", ""),
            "core": entry["core"]  # Add the 'core' data point
        }

        # Add formatted entry to the JSON data list
        json_data.append(formatted_entry)

    # Batch update the sheet with new IDs (only if there are updates)
    if updates:
        worksheet.batch_update(updates)  # More efficient than update_cell()
    print(json.dumps(json_data, indent=4))
    return json_data



def create_flowchart_dependency(data, output_file):
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
        for dependency in item["dependency"]:
            dot.edge(dependency, item["id"], constraint="true", minlen="1")  # Forces vertical placement

    # Save and render the graph
    dot.render(f'../other/{output_file}', cleanup=True)
    print(f"Flowchart saved to {output_file}.png")



# Create the flowchart
create_flowchart_dependency(access_google_sheet(google_creds, sheet_id, sheet_name),sheet_name)

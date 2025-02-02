""" 
OVERVIEW: this code creates a visual tech (technology) tree for techs learned in robotics 
and organizes them based on their dependent techs. this code will:

Example CMD:
python3 -m venv myenv
source myenv/bin/activate 
pip install graphviz gspread gspread-formatting google-auth google-api-python-client google-auth-httplib2 google-auth-oauthlib
pip show graphviz
python3 ./tech_tree.py <path_to_google_api_credentials>.json <google_sheet> userAction

SHARING: the google sheet and the folder in which it lives must be shared with the API email and given 'edit access'
"""
import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
import argparse
from graphviz import Digraph
from gspread_formatting import *


# Set up argument parsing to accept both CSV file path and JSON output file name
parser = argparse.ArgumentParser(description="Convert Arduino Tech Tree CSV to JSON format.")
parser.add_argument("google_creds", help="path to the google json api key")
parser.add_argument("sheet_id", help="google sheet id")
parser.add_argument("userAction", help="options: buildTechnologies buildResources")
args = parser.parse_args()

# Accessing the arguments
google_creds = args.google_creds
sheet_id = args.sheet_id
userAction = args.userAction


def pull_techs_from_google_sheet(json_key_path, sheet_id):
    """
    Fetches and returns Google Sheet data as a structured JSON list.
    If an entry lacks an ID, it generates one that does not conflict with existing IDs.
    
    :param json_key_path: Path to Google service account JSON key file.
    :param sheet_id: The ID of the Google Sheet (from the URL).
    :return: List of dictionaries representing sheet data in the desired format.
    """

    creds = Credentials.from_service_account_file(json_key_path, scopes=["https://www.googleapis.com/auth/spreadsheets"])
    client = gspread.authorize(creds)

    # Open the Google Sheet and select the worksheet
    worksheet = client.open_by_key(sheet_id).worksheet("techs")

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
    # DEBUG print(json.dumps(json_data, indent=4))
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


def create_resources_sheet(json_key_path, sheet_id, json_data):
    """
    Creates or clears a 'resources' sheet in the given Google Sheet 
    and populates it with JSON data, including a formatted title row.
    Ensures no duplication of rows based on 'id', removes rows with 
    IDs not present in the current JSON data, and prints added/removed resources.

    :param json_key_path: Path to Google service account JSON key file.
    :param sheet_id: The ID of the Google Sheet (from the URL).
    :param json_data: List of dictionaries containing resource data.
    """
    doc_template = """
## Overview
Brief description of this learning objective and how it connects to the overall learning objective of the class.

## Resources
Internal or external resources to guide the student on their learning path. Should be enough information for students to complete all projects with.

## Project Template
Include driving question, project objectives, specific deliverables and milestones towards completion.

| Criteria     | Description                                                                                     | Points (1-3) |
|--------------|-------------------------------------------------------------------------------------------------|--------------|
| Understanding| Can you describe what is happening using technical vocabulary? Can you explain this vocabulary to a 5th grader? |              |
| Application  | Have you applied this knowledge in your project? Does it work? Does it work every time?         |              |
| Organization | Have you kept your project organized? Was this thrown together or does each part have a place and a purpose? |              |
"""

    # Authenticate with Google Sheets, Docs and Drive API
    scopes = ["https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/documents"]
    creds = Credentials.from_service_account_file(json_key_path, scopes=scopes)
    client = gspread.authorize(creds)
    drive_service = build('drive', 'v3', credentials=creds)
    docs_service = build('docs', 'v1', credentials=creds)

    # Open the Google Sheet by ID
    spreadsheet = client.open_by_key(sheet_id)

    # Create or select the 'resources' sheet
    try:
        worksheet = spreadsheet.worksheet("resources")
    except gspread.exceptions.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(title="resources", rows="100", cols="10")
    
    # Define headers
    headers = ["name", "id", "doc_link", "project_point_values", "points_required", "core"]

    # Check if the header already exists, and if not, insert it
    headers_exist = headers==worksheet.row_values(2)  # Check if headers are in row 2 (where they should be)
    if not headers_exist:
        # Insert title row
        worksheet.insert_row(["RESOURCES"], index=1)  # First row for merged title
        worksheet.insert_row(headers, index=2)  # Second row for headers
        # Freeze the first two rows
        worksheet.freeze(rows=2)

    # Get all rows in the sheet, excluding the header
    all_rows = worksheet.get_all_values()[2:]  # Exclude title and header
    existing_ids = {row[1]: row_num + 3 for row_num, row in enumerate(all_rows)}  # Map id to row number (index 3 onward)

    # Get list of IDs from the JSON data
    json_ids = {entry.get("id", "") for entry in json_data}

    # Remove rows from the sheet that are not in the JSON data
    rows_to_remove = [row_num for id_value, row_num in existing_ids.items() if id_value not in json_ids]
    if rows_to_remove:
        print("Removed resources:")
        for row_num in sorted(rows_to_remove, reverse=True):  # Remove rows starting from the bottom to avoid shifting
            removed_row = worksheet.row_values(row_num)
            worksheet.delete_rows(row_num)
            print(f"  - Resource with ID: {removed_row[1]}, Name: {removed_row[0]}")
    else:
        print("No entries removed.")

    # Process and insert JSON data into the sheet
    rows = []  # List to hold rows to be added
    existing_ids_in_sheet = {row[1] for row in all_rows}  # Extract existing IDs from sheet
    added_resources = []  # List to track added resources

    for entry in json_data:
        resource_id = entry.get("id", "")
        if resource_id not in existing_ids_in_sheet:
            resource_title = f"{resource_id}-{entry.get('name','')}"
            resource_subtitle = f"{entry.get('type','')}-{entry.get('sub_type','')}"
            doc_link = create_doc_in_subfolder(drive_service, docs_service, sheet_id, "Resources", resource_title, resource_subtitle, doc_template)
            row = [
                entry.get("name", ""),  # name
                resource_id,  # id
                doc_link,  # doc_link (empty for now) ### TODO add create_doc_in_subfolder call###
                "",  # project_point_values (empty for now)
                "",  # points_required (empty for now)
                "TRUE" if entry.get("core", False) else "FALSE"  # core (convert boolean to string)
            ]
            rows.append(row)  # Add row to list of rows to be appended
            added_resources.append(entry)  # Keep track of added resources

    # Batch update rows into the sheet if there are new rows to add
    if rows:
        worksheet.append_rows(rows)
        print("Added resources:")
        for resource in added_resources:
            print(f"  - Resource with ID: {resource['id']}, Name: {resource.get('name', 'N/A')}")
    else:
        print("No entries added.")


def create_doc_in_subfolder(drive_service, docs_service, sheet_id, subfolder_name, title, subtitle, content):
    """
    Creates a simple Google Doc in a subfolder of the folder containing a given Google Sheet.
    - The content is inserted as markdown.
    - If the subfolder exists, it is used; otherwise, a new one is created.
    - If a document with the same title already exists in the subfolder, it is reused instead of creating a new one.
    - The document is made sharable to anyone with the link.

    :param drive_service: Authenticated Google Drive API service.
    :param docs_service: Authenticated Google Docs API service.
    :param sheet_id: The ID of the Google Sheet.
    :param subfolder_name: The name of the subfolder to create (or use) inside the sheet's folder.
    :param title: The title of the document.
    :param subtitle: The subtitle of the document.
    :param content: A list of tuples (header, paragraph) to be added as markdown.
    :return: Sharable link to the created or existing Google Doc.
    """
    try:
        # Step 1: Get the Google Sheet's parent folder
        sheet_metadata = drive_service.files().get(fileId=sheet_id, fields='parents').execute()
        parent_folder_id = sheet_metadata['parents'][0]

        # Step 2: Check if the subfolder already exists
        query = f"'{parent_folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and name='{subfolder_name}'"
        existing_folders = drive_service.files().list(q=query, fields="files(id)").execute().get('files', [])
        
        subfolder_id = existing_folders[0]['id'] if existing_folders else None
        if subfolder_id is None:
            folder_metadata = {'name': subfolder_name, 'mimeType': 'application/vnd.google-apps.folder', 'parents': [parent_folder_id]}
            subfolder = drive_service.files().create(body=folder_metadata, fields='id').execute()
            subfolder_id = subfolder['id']

        # Step 3: Check for existing document
        query = f"'{subfolder_id}' in parents and mimeType='application/vnd.google-apps.document' and name='{title}'"
        existing_docs = drive_service.files().list(q=query, fields="files(id)").execute().get('files', [])
        
        doc_id = existing_docs[0]['id'] if existing_docs else None
        if doc_id is None:
            doc_metadata = {'title': title}
            document = docs_service.documents().create(body=doc_metadata).execute()
            doc_id = document['documentId']
            drive_service.files().update(fileId=doc_id, addParents=subfolder_id).execute()

        # Step 4: Insert the title, subtitle, and content as markdown text
        requests = []
        cursor_index = 1  # Start from index 1 for title

        # Add Title
        requests.append({
            "insertText": {"location": {"index": cursor_index}, "text": title + "\n"}
        })
        cursor_index += len(title) + 1  # Increment cursor index after insertion

        # Add Subtitle
        requests.append({
            "insertText": {"location": {"index": cursor_index}, "text": subtitle + "\n\n"}
        })
        cursor_index += len(subtitle) + 2  # Increment cursor index after insertion

        # Add Content 
        requests.append({
            "insertText": {"location": {"index": cursor_index}, "text": content}
        })

        # Execute Batch Update
        docs_service.documents().batchUpdate(documentId=doc_id, body={"requests": requests}).execute()

        # Step 5: Make the document sharable to anyone with the link
        drive_service.permissions().create(fileId=doc_id, body={'type': 'anyone', 'role': 'reader'}, fields="id").execute()

        # Step 6: Return sharable link
        doc_link = f"https://docs.google.com/document/d/{doc_id}/edit"
        return doc_link

    except HttpError as error:
        print(f"An error occurred: {error}")
        return None


def create_progression_sheet(google_creds, sheet_id):
    print("program yet to be built")


if userAction == "buildResources":
    create_resources_sheet(google_creds, sheet_id, pull_techs_from_google_sheet(google_creds, sheet_id))
if userAction == "buildTechnologies":
    create_flowchart_dependency(pull_techs_from_google_sheet(google_creds, sheet_id),"techs")
if userAction == "buildProgression":
    create_progression_sheet(google_creds, sheet_id)
""" 
OVERVIEW: this code creates a visual tech (technology) tree for techs learned in robotics 
and organizes them based on their dependent techs. this code will:

Example CMD:
python3 -m venv myenv
source myenv/bin/activate 
pip install graphviz gspread gspread-formatting google-auth google-api-python-client google-auth-httplib2 google-auth-oauthlib dash plotly networkx numpy

python3 ./tech_tree.py <path_to_google_api_credentials>.json <google_sheet_id> userAction

SHARING: the google sheet and the folder in which it lives must be shared with the API email and given 'edit access'
"""

import json
import argparse
import gspread
from gspread_formatting import *
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from graphviz import Digraph

# Dash imports
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import networkx as nx
import plotly.graph_objs as go


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
    id_col_index = headers.index("tech_id") + 1  # Find index of the "tech_id" column (1-based for Google Sheets)
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

        # Generate tech ID if missing
        if not entry.get("tech_id"):
            type_prefix = entry["type"][:3].upper()  # First 3 letters of type
            num = type_counters.get(type_prefix, 0) + 1
            new_id = f"{type_prefix}{num:03d}"

            # Ensure ID is unique
            while new_id in existing_ids:
                num += 1
                new_id = f"{type_prefix}{num:03d}"

            # Assign final unique ID
            entry["tech_id"] = new_id
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
            "core": entry["core"],  # Add the 'core' data point
            "tech_id": entry["tech_id"],
            "dependency": entry.get("dependency", []),
            "tech_link": entry.get("tech_link", ""),
            "project_points": entry.get("project_points", ""),
            "required_points": entry.get("required_points", "")
            
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
                sub.node(item["tech_id"], f'{item["name"]}\n({item["tech_id"]})', fillcolor=type_color, width="1", height="0.4")

    # Ensure dependent nodes appear **below** their dependencies
    for item in data:
        for dependency in item["dependency"]:
            dot.edge(dependency, item["tech_id"], constraint="true", minlen="1")  # Forces vertical placement

    # Save and render the graph
    dot.render(f'../other/{output_file}', cleanup=True)
    print(f"Flowchart saved to {output_file}.png")


def create_resources(json_key_path, sheet_id):
    """
    Updates existing rows in the 'techs' sheet by adding document links to IDs that do not have one.
    Does NOT add new IDs, only updates missing document links.

    :param json_key_path: Path to Google service account JSON key file.
    :param sheet_id: The ID of the Google Sheet (from the URL).
    """
    
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/documents"]
    creds = Credentials.from_service_account_file(json_key_path, scopes=scopes)
    client = gspread.authorize(creds)
    drive_service = build('drive', 'v3', credentials=creds)
    docs_service = build('docs', 'v1', credentials=creds)
    
    doc_template = """
    ## Overview
    Brief description of this learning objective and how it connects to the 
    overall learning objective of the class.

    ## Resources
    Internal or external resources to guide the student on their learning 
    path. Should be enough information for students to complete all 
    projects with.

    ## Project Template
    Include driving question, project objectives, specific deliverables and 
    milestones towards completion.

    |--------------|------------------------------------------|--------------|
    | Criteria     | Description                              | Points (1-3) |
    |--------------|------------------------------------------|--------------|
    | Understanding| Can you describe what is happening using |              |
    |              | technical vocabulary? Can you explain    |              |
    |              | this vocabulary to a 5th grader?         |              |
    |--------------|------------------------------------------|--------------|
    | Application  | Have you applied this knowledge in your  |              | 
    |              | project? Does it work? Does it work      |              |  
    |              | every time?                              |              |
    |--------------|------------------------------------------|--------------|
    | Organization | Have you kept your project organized?    |              |
    |              | Was this thrown together or does each    |              |
    |              | part have a place and a purpose?         |              |
    |--------------|------------------------------------------|--------------|
    """

    worksheet = client.open_by_key(sheet_id).worksheet("techs")
    raw_data = worksheet.get_all_values()
    headers = raw_data[1]  # Assuming the second row contains headers
    
    id_col_index = headers.index("tech_id")
    tech_link_col_index = headers.index("tech_link")
    
    updates = []
    
    for i, row in enumerate(raw_data[2:], start=3):  # Data starts from row 3
        resource_id = row[id_col_index].strip()
        tech_link = row[tech_link_col_index].strip()
        
        if resource_id and not tech_link:  # Only process rows with IDs but missing tech_link
            doc_title = f"{resource_id} - {row[headers.index('name')]}"
            doc_sub_title = f"{row[headers.index('type')]} - {row[headers.index('sub_type')]}"
            tech_link = create_doc_in_subfolder(drive_service, docs_service, sheet_id, "Technologies", doc_title, doc_sub_title, doc_template)
            cell_range = f"{chr(65 + tech_link_col_index)}{i}"  # Convert column index to letter
            updates.append({"range": cell_range, "values": [[tech_link]]})
    
    if updates:
        worksheet.batch_update(updates)
        print(f"Updated {len(updates)} missing document links.")
    else:
        print("No missing document links to update.")


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
            tech_link = f"https://docs.google.com/document/d/{doc_id}/edit"
            return tech_link
        else:
            tech_link = f"https://docs.google.com/document/d/{doc_id}/edit"
            print(f"linked previous resource for {title}")
            return tech_link

    except HttpError as error:
        print(f"An error occurred: {error}")
        return None


def create_progression_sheet(google_creds, sheet_id):
    print("program yet to be built")


def create_dash_app(google_creds, sheet_id):
    app = dash.Dash(__name__)

    app.layout = html.Div([
        html.H1("Tech Dependency Flowchart", style={"textAlign": "center"}),

        # Buttons
        html.Button("Update Techs", id="refresh-button", n_clicks=0, style={"margin": "10px"}),
        html.Button("Build Resources", id="build-resources-button", n_clicks=0, style={"margin": "10px"}),

        # Status Output for Build Resources
        html.Div(id="status-output", style={"margin": "10px", "color": "green"}),

        # Hidden Storage for Data
        dcc.Store(id="stored-data"),

        # Graph Component
        dcc.Graph(id="network-graph"),

        # Floating Detail Box
        html.Div(
            id="node-details",
            style={"display": "none", "position": "absolute",
                   "backgroundColor": "white", "border": "1px solid black",
                   "padding": "10px", "zIndex": 1000, "maxWidth": "250px",
                   "boxShadow": "2px 2px 10px rgba(0,0,0,0.2)"},
            children=[
                html.Div(id="node-content"),
                html.Button("X", id="close-button", n_clicks=0, style={"position": "absolute", "top": "5px", "right": "5px"})
            ]
        ),

        # Store to track whether details are open
        dcc.Store(id="details-visible", data=False),
        dcc.Store(id="last-clicked-node", data=None),
        dcc.Store(id="click-reset", data=0)
    ])

    # Callback to build resources
    @app.callback(
        Output("status-output", "children"),
        Input("build-resources-button", "n_clicks"),
        prevent_initial_call=True
    )
    def handle_build_resources(n_clicks):
        if n_clicks > 0:
            create_resources(google_creds, sheet_id)
            return "Resources have been successfully built!"
        return dash.no_update

    # Function to Fetch Data
    def fetch_updated_data():
        """Fetch updated data from Google Sheets"""
        return pull_techs_from_google_sheet(google_creds, sheet_id)

    # Callback to Fetch and Store Data When Refresh Button is Clicked
    @app.callback(
        Output("stored-data", "data"),
        Input("refresh-button", "n_clicks"),
        prevent_initial_call=True
    )
    def update_stored_data(n_clicks):
        return fetch_updated_data()

    # Callback to Update Graph When Data is Updated
    @app.callback(
        Output("network-graph", "figure"),
        Input("stored-data", "data")
    )
    def update_graph(stored_data):
        if not stored_data:
            raise dash.exceptions.PreventUpdate

        # Create Directed Graph
        G = nx.DiGraph()
        node_lookup = {node["tech_id"]: node for node in stored_data}
        edges = []

        for node in stored_data:
            G.add_node(node["tech_id"], label=f"{node['name']} ({node['tech_id']})")
            for dep in node["dependency"]:
                if dep in node_lookup:
                    G.add_edge(dep, node["tech_id"])
                    edges.append((dep, node["tech_id"]))

        # Compute depth levels for nodes (to determine vertical position)
        def compute_depth(node, depth_map):
            if node in depth_map:
                return depth_map[node]
            predecessors = list(G.predecessors(node))
            if not predecessors:  # Root node
                depth_map[node] = 0
            else:
                depth_map[node] = max(compute_depth(parent, depth_map) for parent in predecessors) + 1
            return depth_map[node]

        depth_map = {}
        for node in G.nodes:
            compute_depth(node, depth_map)

        # Assign positions
        pos = {}
        x_positions = {}  # Track used X positions per depth level
        for node, depth in depth_map.items():
            if depth not in x_positions:
                x_positions[depth] = 0
            pos[node] = (x_positions[depth], -depth)  # Higher depth = lower Y
            x_positions[depth] += 1  # Increment X position

        # Create Plotly Edges
        edge_traces = [
            go.Scatter(
                x=[pos[edge[0]][0], pos[edge[1]][0], None],
                y=[pos[edge[0]][1], pos[edge[1]][1], None],
                line=dict(width=1, color="gray"),
                mode="lines"
            ) for edge in edges
        ]

        # Create Plotly Nodes
        node_traces = [
            go.Scatter(
                x=[x], y=[y],
                text=node_lookup[node_id]["name"] + f" ({node_id})",
                mode="markers+text",
                textposition="top center",
                marker=dict(size=20, color="blue"),
                hoverinfo="text",
                customdata=[node_id]
            ) for node_id, (x, y) in pos.items()
        ]

        return go.Figure(
            data=edge_traces + node_traces,
            layout=go.Layout(
                showlegend=False, hovermode="closest",
                margin=dict(b=0, l=0, r=0, t=0),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            )
        )


    @app.callback(
        [Output("node-content", "children"), 
         Output("node-details", "style"), 
         Output("details-visible", "data"), 
         Output("last-clicked-node", "data"),
         Output("network-graph", "clickData")],  # Reset clickData
        [Input("network-graph", "clickData"), 
         Input("close-button", "n_clicks")],
        [State("stored-data", "data")]
    )
    def display_node_details(clickData, n_clicks_close, stored_data):
        ctx = dash.callback_context
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else None

        # If close button clicked, reset everything
        if trigger_id == "close-button":
            return "", {"display": "none"}, False, None, None  # Reset clickData too!

        # If no node clicked or no data available, do nothing
        if not clickData or not stored_data:
            return dash.no_update

        # Get clicked node ID
        node_id = clickData["points"][0]["customdata"]

        # Find node details
        node_lookup = {node["tech_id"]: node for node in stored_data}
        node_info = node_lookup.get(node_id, {})

        # Ensure node details exist
        if not node_info:
            return dash.no_update

        # Get click position
        x_click, y_click = clickData["points"][0]["x"], clickData["points"][0]["y"]

        new_style = {
            "display": "block",
            "position": "absolute",
            "left": f"{x_click * 50 + 300}px",
            "top": f"{y_click * 50 + 300}px",
            "backgroundColor": "white",
            "border": "1px solid black",
            "padding": "10px",
            "zIndex": 1000,
            "maxWidth": "250px",
            "boxShadow": "2px 2px 10px rgba(0,0,0,0.2)"
        }

        node_details_content = html.Div([
            html.H3(f"{node_info['name']} ({node_info['tech_id']})"),
            html.P(f"Type: {node_info['type']}"),
            html.P(f"Sub-Type: {node_info['sub_type']}"),
            html.P(f"Core Component: {'Yes' if node_info['core'] else 'No'}"),
            html.P(f"Dependencies: {', '.join(node_info['dependency']) if node_info['dependency'] else 'None'}"),
            html.P(f"Project Point Values: {node_info['project_points']}"),
            html.P(f"Points Required: {node_info['required_points']}"),
            html.A("Open Document", href=node_info["tech_link"], target="_blank")
        ])

        return node_details_content, new_style, True, node_id, clickData  # Keep clickData!


    return app


def save_json(data, filename="data.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def load_json(filename="data.json"):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}  # Return an empty dictionary if file doesn't exist


if userAction == "runServer":
    # define filenames
    local_json_files = {
        "techs":"techTree_techs.json",
        "materials":"techTree_materials.json",
        "projects":"techTree_projects.json",
        "progress":"techTree_progress.json",
        "kits":"techTree_kits.json",
        "contracts":"techTree_contracts.json"
    }
    if __name__ == "__main__":
        app = create_dash_app(google_creds, sheet_id)
        app.run_server(debug=True)
if userAction == "buildResources":
    create_resources(google_creds, sheet_id)
if userAction == "buildTechnologies":
    create_flowchart_dependency(pull_techs_from_google_sheet(google_creds, sheet_id),"techs")
if userAction == "buildProgression":
    create_progression_sheet(google_creds, sheet_id)
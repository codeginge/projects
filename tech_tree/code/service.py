import dash
import dash_cytoscape as cyto
import json
import uuid
import datetime
import os
from dash import dcc, html, Input, Output, State, ctx, no_update
from flask import Flask, session
from dash.dependencies import ALL, MATCH

# ---------- Load Data ----------
with open("/Users/michael/Desktop/status_data.json") as f:
    user_data = json.load(f)

with open("/Users/michael/Desktop/ims_data.json") as f:
    lms_data = json.load(f)

UPDATE_LOG_PATH = "/Users/michael/Desktop/updates_log.json"

# Lookup tables
users = {user["username"]: user for user in user_data}
lms_lookup = {item["id"]: item for item in lms_data}

# Map prefixes to friendly names
CATEGORY_NAMES = {
    't': 'Techs',
    'p': 'Projects',
    'c': 'Contracts'
}


def build_dependency_graph(user, category):
    """
    Build a Dash Cytoscape component representing dependencies as a root system.

    :param user: The viewing user dict
    :param category: 't', 'p', or 'c' for the tab category
    :return: dash_cytoscape.Cytoscape component
    """
    raw_items = [item for item in user.get("raw_data", []) if item["id"].lower().startswith(category)]
    item_ids_in_category = {item["id"] for item in raw_items}

    # Build nodes with a multiline label
    nodes = []
    for item in raw_items:
        lms_item = lms_lookup.get(item["id"], {})
        name = lms_item.get("name", "N/A")
        item_type = lms_item.get("type", "N/A")
        sub_type = lms_item.get("sub_type", "N/A")

        # Create a formatted label with newlines
        label = (
            f"{item['id']} ({item.get('points', 0)} pts)\n"
            f"{name}\n"
            f"{item_type} - {sub_type}"
        )
        nodes.append({
            "data": {"id": item["id"], "label": label},
            "classes": category
        })

    # Build edges based on dependencies from lms_data
    edges = []
    for item in raw_items:
        lms_item = lms_lookup.get(item["id"])
        if lms_item:
            dep_id = lms_item.get("dependency", "")
            if dep_id and dep_id in item_ids_in_category:
                edges.append({"data": {"source": dep_id, "target": item["id"]}})

    elements = nodes + edges

    # Use 'dagre' only if there are edges. Otherwise, use a simple 'grid' layout.
    if edges:
        cyto_layout = {
            'name': 'dagre',
            'rankDir': 'TB',  # Top-to-Bottom
            'padding': 10
        }
    else:
        cyto_layout = {
            'name': 'grid',
            'rows': 5
        }

    stylesheet = [
        {"selector": 'node', "style": {
            "content": "data(label)",
            "text-valign": "center",
            "text-halign": "center",
            "shape": "round-rectangle",
            "background-color": "#97C2FC",
            "padding": "10px",
            "text-wrap": "wrap",
            "text-max-width": "120px",  # This ensures the text doesn't go beyond a certain width
            "width": "150px",  # Sets a base width for all nodes
            "height": "80px",  # Sets a base height for all nodes
            "min-height": "40px",  # Allows the box to shrink if the text is small
            "min-width": "100px"  # Allows the box to shrink if the text is small
        }},
        {"selector": 'edge', "style": {
            "line-color": "#888",
            "target-arrow-color": "#888",
            "target-arrow-shape": "triangle",
            "curve-style": "bezier"
        }},
        {"selector": ".t", "style": {"background-color": "#F4A261"}},
        {"selector": ".p", "style": {"background-color": "#2A9D8F"}},
        {"selector": ".c", "style": {"background-color": "#E76F51"}},
    ]

    cyto_graph = cyto.Cytoscape(
        id={"type": "cytoscape-graph", "category": category},
        elements=elements,
        layout=cyto_layout,
        stylesheet=stylesheet,
        style={"width": "100%", "height": "600px"}
    )

    return cyto_graph


def append_update_log(new_entry):
    if os.path.exists(UPDATE_LOG_PATH):
        with open(UPDATE_LOG_PATH, "r") as f:
            try:
                data = json.load(f)
            except:
                data = []
    else:
        data = []

    data.append(new_entry)

    with open(UPDATE_LOG_PATH, "w") as f:
        json.dump(data, f, indent=4)


# ---------- Flask / Dash ----------
server = Flask(__name__)
server.secret_key = str(uuid.uuid4())

app = dash.Dash(__name__, server=server, suppress_callback_exceptions=True)
cyto.load_extra_layouts()

# ---------- Pages ----------
def login_page():
    return html.Div([
        html.H2("Login"),
        dcc.Input(id='username', placeholder='Username', type='text'),
        dcc.Input(id='password', placeholder='Password', type='password'),
        html.Button("Login", id="login-btn"),
        html.Div(id="login-message")
    ])

def dashboard_page(user):
    prefixes = sorted(set(item['id'][0].lower()
                             for item in user.get('raw_data', [])
                             if 'id' in item and item['id']))

    tabs = []
    for prefix in prefixes:
        filtered_items = [i for i in user['raw_data'] if i['id'].lower().startswith(prefix)]
        label = f"{CATEGORY_NAMES.get(prefix, prefix.upper())} ({len(filtered_items)})"
        tabs.append(dcc.Tab(label=label, value=prefix))

    tabs.append(dcc.Tab(label=f"Raw Data ({len(user.get('raw_data', []))})", value='raw'))

    teacher_dropdown = []
    if user.get("type") == "teacher":
        teacher_dropdown = [
            html.Label("Select User to View:"),
            dcc.Dropdown(
                id="teacher-user-select",
                options=[
                    {"label": f"{u['first'].title()} {u['last'].title()} ({uname})", "value": uname}
                    for uname, u in users.items()
                ],
                value=user["username"],  # default to themselves
                clearable=False
            ),
            html.Hr()
        ]

    return html.Div([
        dcc.Store(
            id="user-data",
            data={"logged_in": user, "viewing": user}
        ),
        html.H2(f"Welcome, {user['first'].title()} {user['last'].title()}!"),
        html.P(f"User Type: {user['type']}"),
        html.Button("Log out", id="logout-btn"),
        html.Hr(),

        html.H4("Data Browser"),
        # FIX: The teacher_dropdown is already a list, so it's correct.
        # The issue lies in the callback that updates it, or a separate issue.
        # This part of the code is fine, but it was a potential point of failure.
        *teacher_dropdown,  # Unpack the list of components here
        dcc.Tabs(id="data-tabs", value=tabs[0].value if tabs else 'raw', children=tabs),
        html.Div(id="tab-content", style={"marginTop": "20px"}),

        # Modal for item details
        html.Div(
            id="modal",
            style={
                "display": "none",
                "position": "fixed",
                "top": "50%",
                "left": "50%",
                "transform": "translate(-50%, -50%)",
                "backgroundColor": "white",
                "padding": "20px",
                "boxShadow": "0 4px 8px rgba(0,0,0,0.2)",
                "zIndex": 1000
            }
        ),
        html.Div(
            id="modal-backdrop",
            style={
                "display": "none",
                "position": "fixed",
                "top": 0,
                "left": 0,
                "width": "100%",
                "height": "100%",
                "backgroundColor": "rgba(0,0,0,0.5)",
                "zIndex": 999
            }
        )
    ])


# ---------- Layout ----------
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# ---------- Callbacks ----------
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname):
    user = session.get("user")
    if pathname == "/dashboard" and user:
        return dashboard_page(user)
    return login_page()

@app.callback(
    Output("login-message", "children"),
    Output("url", "pathname", allow_duplicate=True),
    Input("login-btn", "n_clicks"),
    State("username", "value"),
    State("password", "value"),
    prevent_initial_call=True
)
def handle_login(n_clicks, username, password):
    user = users.get(username)
    if user and user["password"] == password:
        session["user"] = user
        return "", "/dashboard"
    return "Invalid credentials", no_update

@app.callback(
    Output("url", "pathname", allow_duplicate=True),
    Input("logout-btn", "n_clicks"),
    prevent_initial_call=True
)
def logout(n_clicks):
    session.pop("user", None)
    return "/"

@app.callback(
    Output("tab-content", "children"),
    Input("data-tabs", "value"),
    State("user-data", "data"),
    prevent_initial_call=False
)
def render_tab(tab_value, stored):
    if not stored or not stored.get("viewing"):
        return html.Div("No user logged in.")

    viewing_user = stored["viewing"]

    if tab_value == 'raw':
        return html.Ul([
            html.Li(
                dcc.Link(
                    f"{item['id']}: {item.get('points', 0)} pts — {item.get('comments', '')}",
                    id={"type": "item-link", "index": item['id']},
                    href="#"
                )
            )
            for item in viewing_user['raw_data']
        ])
    
    # Check if a category tab is selected
    if tab_value in CATEGORY_NAMES:
        graph_component = build_dependency_graph(viewing_user, tab_value)
        return html.Div([graph_component])
    
    return html.Div("No content to display for this tab.")


def open_modal_content(item_id, stored):
    if not stored or not item_id:
        return no_update

    logged_in_user = stored["logged_in"]
    viewing_user = stored["viewing"]

    details = lms_lookup.get(item_id, {})

    # Find the specific item for this user
    user_item = {}
    for item in viewing_user.get("raw_data", []):
        if item.get("id", "").lower() == item_id.lower():
            user_item = item
            break
    
    # Helper to render LMS data list
    def make_ul(data_dict, title):
        if not data_dict:
            return html.Div()
        items = []
        for k, v in data_dict.items():
            if k == "doc_link" and v:
                items.append(html.Li([
                    f"{k}: ",
                    html.A("Link", href=v, target="_blank", style={"color": "blue", "textDecoration": "underline"})
                ]))
            else:
                items.append(html.Li(f"{k}: {v}"))
        return html.Div([html.H5(title), html.Ul(items)])

    lms_section = make_ul(details, "LMS Data")

    # Base section with current values
    user_section_children = [
        html.H5("User Data"),
        html.Ul([
            html.Li(f"Points: {user_item.get('points', 'N/A')}"),
            html.Li(f"Comments: {user_item.get('comments', '') or 'None'}"),
        ])
    ]

    # Teacher: can edit points
    if logged_in_user.get("type") == "teacher":
        user_section_children.append(
            html.Div([
                html.Label("Edit Points:"),
                dcc.Input(
                    id={"type": "modal-points-input", "index": item_id},
                    type="number",
                    min=0,
                    step=1,
                    value=user_item.get("points", 0)
                ),
                html.Button("Save Points", id={"type": "save-points-btn", "index": item_id}, n_clicks=0)
            ], style={"marginTop": "20px"})
        )

    # Student viewing own data: can add comment
    elif (
        logged_in_user.get("type") == "student"
        and logged_in_user["username"] == viewing_user["username"]
    ):
        user_section_children.append(
            html.Div([
                html.Label("Add Comment:"),
                dcc.Textarea(
                    id={"type": "modal-comment-input", "index": item_id},
                    value="",
                    style={"width": "100%", "height": 100}
                ),
                html.Button("Save Comment", id={"type": "save-comment-btn", "index": item_id}, n_clicks=0)
            ], style={"marginTop": "20px"})
        )

    # Wrap sections
    user_section = html.Div(user_section_children)

    # Hidden data for saving callbacks
    hidden_data = html.Div([
        dcc.Store(id="modal-user-id", data=viewing_user["username"]),
        dcc.Store(id="modal-item-id", data=item_id)
    ])

    # Full modal body
    body = html.Div([lms_section, user_section, hidden_data])

    return html.Div([
        html.H3(f"Details for {item_id}"),
        body,
        html.Button("Close", id={"type": "close-modal", "index": item_id}, n_clicks=0, style={"marginTop": "20px"})
    ])

@app.callback(
    Output("modal", "children"),
    Output("modal", "style"),
    Output("modal-backdrop", "style"),
    Input({"type": "item-link", "index": ALL}, "n_clicks"),
    Input({"type": "cytoscape-graph", "category": ALL}, "tapNodeData"),
    Input({"type": "close-modal", "index": ALL}, "n_clicks"),
    Input({"type": "save-comment-btn", "index": ALL}, "n_clicks"),
    Input({"type": "save-points-btn", "index": ALL}, "n_clicks"),
    State({"type": "modal-comment-input", "index": ALL}, "value"),
    State({"type": "modal-points-input", "index": ALL}, "value"),
    State("user-data", "data"),
    prevent_initial_call=True
)
def handle_modal_actions(item_links_clicks, cytoscape_node_data_list, close_clicks, save_comment_clicks, save_points_clicks,
                          comment_value_list, points_value_list, stored):
    trigger = ctx.triggered_id
    if not trigger:
        return no_update, no_update, no_update

    item_id = None
    if isinstance(trigger, dict):
        item_id = trigger.get("index")

    if isinstance(trigger, dict) and trigger["type"] == "close-modal":
        return None, {"display": "none"}, {"display": "none"}
    
    if isinstance(trigger, dict) and trigger["type"] == "save-comment-btn":
        if any(save_comment_clicks) and item_id and stored:
            comment_value = None
            for i, click in enumerate(save_comment_clicks):
                if click:
                    comment_value = comment_value_list[i]
                    break

            update_entry = {
                "username": stored["viewing"]["username"],
                "item_id": item_id,
                "timestamp": datetime.datetime.now().isoformat(),
                "comment": comment_value or ""
            }
            append_update_log(update_entry)
            return None, {"display": "none"}, {"display": "none"}
    
    if isinstance(trigger, dict) and trigger["type"] == "save-points-btn":
        if any(save_points_clicks) and item_id and stored:
            points_value = None
            for i, click in enumerate(save_points_clicks):
                if click:
                    points_value = points_value_list[i]
                    break

            try:
                points_value_int = int(points_value)
            except (TypeError, ValueError):
                points_value_int = None
            
            update_entry = {
                "username": stored["viewing"]["username"],
                "item_id": item_id,
                "timestamp": datetime.datetime.now().isoformat(),
                "points": points_value_int
            }
            append_update_log(update_entry)
            return None, {"display": "none"}, {"display": "none"}

    item_id_to_open = None
    if isinstance(trigger, dict) and trigger.get("type") == "item-link":
        item_id_to_open = trigger.get("index")
    elif isinstance(trigger, dict) and trigger.get("type") == "cytoscape-graph":
        if cytoscape_node_data_list:
            for data in cytoscape_node_data_list:
                if data:
                    item_id_to_open = data.get("id")
                    break
    
    if item_id_to_open:
        content = open_modal_content(item_id_to_open, stored)
        modal_style = {
            "display": "block",
            "position": "fixed",
            "top": "50%",
            "left": "50%",
            "transform": "translate(-50%, -50%)",
            "backgroundColor": "white",
            "padding": "20px",
            "boxShadow": "0 4px 8px rgba(0,0,0,0.2)",
            "zIndex": 1000,
            "maxWidth": "600px",
            "width": "90%",
            "overflowY": "auto",
            "maxHeight": "80vh"
        }
        backdrop_style = {
            "display": "block",
            "position": "fixed",
            "top": 0,
            "left": 0,
            "width": "100%",
            "height": "100%",
            "backgroundColor": "rgba(0,0,0,0.5)",
            "zIndex": 999,
        }
        return content, modal_style, backdrop_style
    
    return no_update, no_update, no_update


@app.callback(
    Output("user-data", "data", allow_duplicate=True),
    Output("data-tabs", "value", allow_duplicate=True),
    Output("data-tabs", "children", allow_duplicate=True),
    Input("teacher-user-select", "value"),
    State("user-data", "data"),
    prevent_initial_call=True
)
def update_selected_user(selected_username, stored):
    if not selected_username or selected_username not in users:
        return no_update, no_update, no_update

    logged_in_user = stored["logged_in"]
    viewing_user = users[selected_username]

    prefixes = sorted(set(item['id'][0].lower()
                             for item in viewing_user.get('raw_data', [])
                             if 'id' in item and item['id']))
    tabs = []
    for prefix in prefixes:
        filtered_items = [i for i in viewing_user['raw_data'] if i['id'].lower().startswith(prefix)]
        label = f"{CATEGORY_NAMES.get(prefix, prefix.upper())} ({len(filtered_items)})"
        tabs.append(dcc.Tab(label=label, value=prefix))
    tabs.append(dcc.Tab(label=f"Raw Data ({len(viewing_user.get('raw_data', []))})", value='raw'))
    
    return {"logged_in": logged_in_user, "viewing": viewing_user}, tabs[0].value if tabs else 'raw', tabs


# ---------- Run ----------
if __name__ == '__main__':
    app.run(debug=True)
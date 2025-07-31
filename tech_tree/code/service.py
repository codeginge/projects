import dash
from dash import dcc, html, Input, Output, State, ctx
import json
from flask import Flask, session
import uuid

# Load your user data
with open("/Users/michael/Desktop/status_data.json") as f:
    user_data = json.load(f)

# Create user lookup by username
users = {user["username"]: user for user in user_data}

# Create a Flask server
server = Flask(__name__)
server.secret_key = str(uuid.uuid4())  # Needed for session

# Create Dash app
app = dash.Dash(__name__, server=server, suppress_callback_exceptions=True)

# Pages
def login_page():
    return html.Div([
        html.H2("Login"),
        dcc.Input(id='username', placeholder='Username', type='text'),
        dcc.Input(id='password', placeholder='Password', type='password'),
        html.Button("Login", id="login-btn"),
        html.Div(id="login-message")
    ])

def dashboard_page(user):
    return html.Div([
        html.H2(f"Welcome, {user['first'].title()} {user['last'].title()}!"),
        html.P(f"User Type: {user['type']}"),
        html.Button("Log out", id="logout-btn"),
        html.Hr(),
        html.H4("Raw Data"),
        html.Ul([
            html.Li(f"{item['id']}: {item['points']} pts — {item['comments']}")
            for item in user['raw_data']
        ])
    ])

# Layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Callbacks
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname):
    if pathname == "/dashboard" and session.get("user"):
        return dashboard_page(session["user"])
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
    return "Invalid credentials", dash.no_update

@app.callback(
    Output("url", "pathname"),
    Input("logout-btn", "n_clicks"),
    prevent_initial_call=True
)
def logout(n_clicks):
    session.pop("user", None)
    return "/"

if __name__ == '__main__':
    app.run_server(debug=True)

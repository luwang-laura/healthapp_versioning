#!/usr/bin/env python3
"""
Health Analytics Dashboard Application - Fixed Version
"""

import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import base64
import io
import pandas as pd

# Import data modules
try:
from load_data0 import get_data0
from load_data1 import get_data1
from load_data2 import get_data2
from load_data3 import get_data3
from load_data4 import get_data4
except ImportError:
# Define placeholder functions if modules don't exist
def get_data0(*args): return [html.Div(), html.Div(), html.Div()]
def get_data1(*args): return [html.Div(), html.Div(), html.Div()]
def get_data2(*args): return [html.Div(), html.Div(), html.Div()]
def get_data3(*args): return [html.Div(), html.Div(), html.Div()]
def get_data4(*args): return [html.Div(), html.Div(), html.Div()]

# Initialize the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Global variables
file_name = None
button_id_all = None

# Initialize global display components
ga = [html.Div("Component A1", style={'padding': '10px', 'border': '1px solid #ddd'}),
html.Div("Component A2", style={'padding': '10px', 'border': '1px solid #ddd'}),
html.Div("Component A3", style={'padding': '10px', 'border': '1px solid #ddd'})]
gb = [html.Div("Component B1", style={'padding': '10px', 'border': '1px solid #ddd'}),
html.Div("Component B2", style={'padding': '10px', 'border': '1px solid #ddd'}),
html.Div("Component B3", style={'padding': '10px', 'border': '1px solid #ddd'})]
gc = [html.Div("Component C1", style={'padding': '10px', 'border': '1px solid #ddd'}),
html.Div("Component C2", style={'padding': '10px', 'border': '1px solid #ddd'}),
html.Div("Component C3", style={'padding': '10px', 'border': '1px solid #ddd'})]
a, b, c = ga, gb, gc

colors = {
'background': '#f8f9fa',
'text': '#212529'
}

# Select component
select1 = dbc.Select(
id="Xvariable",
options=[
{"label": "Option 1", "value": "1"},
{"label": "Option 2", "value": "2"},
{"label": "Disabled option", "value": "3", "disabled": True},
],
)

def parse_contents(contents, filename, date):
"""Parse uploaded CSV file contents"""
if contents is None:
return None

content_type, content_string = contents.split(',')
decoded = base64.b64decode(content_string)

try:
if 'csv' in filename.lower():
df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
return df
else:
return pd.DataFrame()
except Exception as e:
print(f"Error parsing file: {e}")
return pd.DataFrame()

# Upload component - FIXED: db.Button to dbc.Button
up_file = dcc.Upload(
id='upload-data',
children=dbc.Button('Upload File', color="primary", className="w-100"),
multiple=False
)

# Button components - FIXED: Removed block=True, added className="w-100"
Button1 = dbc.Button("Statistical Approach", id='b1', color="primary", className="w-100")
Button2 = dbc.Button("Machine Learning Models", id='b2', color="secondary", className="w-100")
Button3 = dbc.Button("Compare average", id='b3', color="success", className="w-100")
Button5 = dbc.Button("File Status", id='b6', color="info", className="w-100")

# File upload callback
@app.callback(
Output(component_id='b6', component_property='children'),
Input('upload-data', 'contents'),
State('upload-data', 'filename'),
State('upload-data', 'last_modified')
)
def update_output(contents, filename, last_modified):
"""Handle file upload and update button text"""
print(f"Upload - Contents: {contents is not None}, Filename: {filename}")

if contents is None:
return 'No file uploaded'

if filename is not None:
global file_name
file_name = parse_contents(contents, filename, last_modified)

if file_name is not None and not file_name.empty:
# Update dropdown options with column names
name_list = file_name.columns.tolist() if not file_name.empty else []
if name_list:
# You can use these to update another component if needed
print(f"Columns found: {name_list}")
return f"File: {filename[-15:]}"
else:
return "Upload failed"

return "Upload a file"

# Layout
leftButton = html.Div([
html.H1(
children='Interactive Health Analytic Dashboard',
style={
'textAlign': 'center',
'color': colors['text'],
'marginBottom': '30px',
'marginTop': '20px'
}
),

# First row - Controls
dbc.Row([
dbc.Col(html.Div([up_file]), width=2, md=2, sm=12),
dbc.Col(Button5, width=2, md=2, sm=12),
dbc.Col(Button1, width=2, md=2, sm=12),
dbc.Col(Button2, width=2, md=2, sm=12),
dbc.Col(Button3, width=2, md=2, sm=12),
], className="mb-4 g-2", justify="center"),

# Variable selection row
dbc.Row([
dbc.Col([html.Label("Select X Variable:"), select1], width=4)
], className="mb-4"),

# First row of outputs
dbc.Row([
dbc.Col(html.Div(id='11', children=[a[0]]), width=4),
dbc.Col(html.Div(id='12', children=[b[0]]), width=4),
dbc.Col(html.Div(id='13', children=[b[0]]), width=4),
], className="mb-3"),

# Second row of outputs
dbc.Row([
dbc.Col(html.Div(id='21', children=[a[1]]), width=4),
dbc.Col(html.Div(id='22', children=[b[1]]), width=4),
dbc.Col(html.Div(id='23', children=[c[1]]), width=4),
], className="mb-3"),

# Third row of outputs
dbc.Row([
dbc.Col(html.Div(id='31', children=[a[2]]), width=4),
dbc.Col(html.Div(id='32', children=[b[2]]), width=4),
dbc.Col(html.Div(id='33', children=[c[2]]), width=4),
], className="mb-3"),
])

# Main callback for button interactions
@app.callback(
Output(component_id='11', component_property='children'),
Output(component_id='12', component_property='children'),
Output(component_id='13', component_property='children'),
Output(component_id='21', component_property='children'),
Output(component_id='22', component_property='children'),
Output(component_id='23', component_property='children'),
Output(component_id='31', component_property='children'),
Output(component_id='32', component_property='children'),
Output(component_id='33', component_property='children'),
Input('b1', 'n_clicks'),
Input('b2', 'n_clicks'),
Input('b3', 'n_clicks'),
)
def display(btn1, btn2, btn3):
"""Handle button clicks and update displays"""
ctx = dash.callback_context

if not ctx.triggered:
button_id = 'No clicks yet'
else:
button_id = ctx.triggered[0]['prop_id'].split('.')[0]
print(f"Button clicked: {button_id}")

global button_id_all
if button_id_all is None and button_id != 'No clicks yet':
button_id_all = button_id

if button_id not in ('b1', 'b2', 'b3'):
if button_id_all:
button_id = button_id_all
else:
button_id = 'b1' # Default to b1

global ga, gb, gc
global file_name

# Default values
result_a, result_b, result_c = ga, gb, gc

# Only process if we have a file
if file_name is not None and isinstance(file_name, pd.DataFrame) and not file_name.empty:
try:
if button_id == 'b1':
data_result = get_data1(file_name)
if data_result and len(data_result) >= 3:
result_a, result_b, result_c = data_result
elif button_id == 'b2':
data_result = get_data2(file_name)
if data_result and len(data_result) >= 3:
result_a, result_b, result_c = data_result
elif button_id == 'b3':
data_result = get_data3(file_name)
if data_result and len(data_result) >= 3:
result_a, result_b, result_c = data_result
except Exception as e:
print(f"Error in data processing: {e}")
error_div = html.Div(f"Error: {str(e)[:50]}", style={'color': 'red'})
result_a = [error_div, error_div, error_div]
result_b = [error_div, error_div, error_div]
result_c = [error_div, error_div, error_div]

return (result_a[0], result_b[0], result_c[0],
result_a[1], result_b[1], result_c[1],
result_a[2], result_b[2], result_c[2])

# Set app layout - FIXED: Removed 'mian' string
app.layout = dbc.Container([leftButton], fluid=True)

if __name__ == '__main__':
# Run the app - FIXED: Added host='0.0.0.0' for EC2 access
app.run_server(debug=True, host='0.0.0.0', port=8050)
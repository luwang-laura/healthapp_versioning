import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import base64
import io
import pandas as pd

# Import your data modules
from load_data0 import get_data0
from load_data1 import get_data1
from load_data2 import get_data2
from load_data3 import get_data3
from load_data4 import get_data4

# Initialize the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Global variables
global file_name
file_name = None
global button_id_all
button_id_all = None

global ga, gb, gc
ga = [html.Hr(), html.Hr(), html.Hr()]
gb = [html.Hr(), html.Hr(), html.Hr()]
gc = [html.Hr(), html.Hr(), html.Hr()]
a, b, c = ga, gb, gc

colors = {
'background': '#111111',
'text': '#111111'
}

def parse_contents(contents, filename, date):
content_type, content_string = contents.split(',')
decoded = base64.b64decode(content_string)

try:
if 'csv' in filename:
# Assume that the user uploaded a CSV file
df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
return df
else:
return pd.DataFrame() # Return empty dataframe for non-csv files
except Exception as e:
print(e)
return pd.DataFrame()

@app.callback(
Output(component_id='b6', component_property='children'),
Input('upload-data', 'contents'),
State('upload-data', 'filename'),
State('upload-data', 'last_modified')
)
def update_output(contents, filename, last_modified):
print(contents, filename, last_modified)
if contents is None:
return 'No file uploaded'
if filename is not None:
global file_name
file_name = parse_contents(contents, filename, last_modified)
if not file_name.empty:
return f"Uploaded: {filename[-15:]}"
else:
return "Upload failed"
return "Upload a file"

# UI Components
up_file = dcc.Upload(
id='upload-data',
children=dbc.Button('Upload File', color="primary", className="w-100")
)

Button1 = dbc.Button("Statistical Approach", id='b1', color="primary", className="w-100")
Button2 = dbc.Button("Machine Learning Models", id='b2', color="secondary", className="w-100")
Button3 = dbc.Button("Compare average", id='b3', color="success", className="w-100")
Button5 = dbc.Button("File Status", id='b6', color="info", className="w-100")

leftButton = html.Div(children=[
html.H1(
children='Interactive Health Analytic Dashboard',
style={
'textAlign': 'center',
'color': colors['text']
}
),
dbc.Row([
dbc.Col(html.Div([up_file]), width=2),
dbc.Col(Button5, width=2),
dbc.Col(Button1, width=2),
dbc.Col(Button2, width=2),
dbc.Col(Button3, width=2),
], className="mb-3"),

dbc.Row([
dbc.Col(html.Div(id='11', children=[a[0]]), width=4),
dbc.Col(html.Div(id='12', children=[b[0]]), width=4),
dbc.Col(html.Div(id='13', children=[b[0]]), width=4),
], className="mb-3"),

dbc.Row([
dbc.Col(html.Div(id='21', children=[a[1]]), width=4),
dbc.Col(html.Div(id='22', children=[b[1]]), width=4),
dbc.Col(html.Div(id='23', children=[c[1]]), width=4),
], className="mb-3"),

dbc.Row([
dbc.Col(html.Div(id='31', children=[a[2]]), width=4),
dbc.Col(html.Div(id='32', children=[b[2]]), width=4),
dbc.Col(html.Div(id='33', children=[c[2]]), width=4),
], className="mb-3"),
])

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
ctx = dash.callback_context

if not ctx.triggered:
button_id = 'No clicks yet'
else:
button_id = ctx.triggered[0]['prop_id'].split('.')[0]
print(f"Button clicked: {button_id}")

global button_id_all
if button_id_all is None and button_id not in ('No clicks yet'):
button_id_all = button_id

if button_id not in ('b1', 'b2', 'b3'):
if button_id_all:
button_id = button_id_all
else:
button_id = 'b1' # Default to b1

global ga, gb, gc
global file_name

# Default values
a, b, c = ga, gb, gc

# Only process if we have a file
if file_name is not None and isinstance(file_name, pd.DataFrame) and not file_name.empty:
try:
if button_id == 'b1':
result = get_data1(file_name)
if result and len(result) >= 3:
a, b, c = result
elif button_id == 'b2':
result = get_data2(file_name)
if result and len(result) >= 3:
a, b, c = result
elif button_id == 'b3':
result = get_data3(file_name)
if result and len(result) >= 3:
a, b, c = result
except Exception as e:
print(f"Error in data processing: {e}")
# Keep default values on error

return a[0], b[0], c[0], a[1], b[1], c[1], a[2], b[2], c[2]

app.layout = dbc.Container([leftButton], fluid=True)

if __name__ == '__main__':
app.run_server(debug=True, host='0.0.0.0', port=8050)
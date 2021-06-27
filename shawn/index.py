import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from app import app
from apps import app1, app2, app3

#if unsure please look at dash multi page layout under dash plotly documentation


# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "14rem",
    "padding": "2rem 1rem",
    "background-color": "#000000",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "14rem",
    "margin-right": "0rem",
    "padding": "1rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Topic Model", className="display-4"),
        html.Hr(),
        html.P(
            "A simple sidebar layout with navigation links", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Word Cloud", href="/apps/app1", active="exact"),
                dbc.NavLink("Sentences and Topics", href="/apps/app2", active="exact"),
                dbc.NavLink("Sentences by Project", href="/apps/app3", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)


app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

@app.callback(Output('page-content', 'children'), Input('url','pathname'))

def display_page(pathname):
    if pathname == '/apps/app1':
        return app1.layout
    elif pathname == '/apps/app2':
        return app2.layout  
    else:
        return app1.layout



if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0') 

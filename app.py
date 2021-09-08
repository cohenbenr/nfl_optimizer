#Core modules
import pandas as pd
import os

#Dash modules
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go

#Custom modules
from optimizer import *
from transform_elo import *
from util_functions import *
from get_elo_data import *

# Colours
# Dark Grey #5d5c61
# Light Grey #39683
# Light blue #7395ae
# Dark blue #557a95
# Sand #b1a296

app = dash.Dash('NFL Survivor Pool Optimiser')
# app.config.suppress_callback_exceptions = True
app.title = 'BGSE NFL Survivor Pool Optimiser'


# Get data
#getLatestELOData()

mydata = pd.read_csv('data/elo/nfl_elo.csv')
static_df = pd.read_csv('data/nfl_lookup_table.csv')
longdata = transform_elo_data(mydata)
optimizer = Optimizer(longdata)
teams = static_df['ShortCode']
SEASON_LENGTH = 17
weeks = list(range(1, SEASON_LENGTH + 1))
target_weeks = list(range(1, SEASON_LENGTH + 1))
thumbnails = initialize_thumbnails(static_df)

#Initialize Params
blocked_teams = []

app.layout = \
    html.Div(className="container", children=[
        dbc.Row(dbc.Col(html.Div(className="mast_head",
                                 children=[html.H1(className="mast_head",
                                                   children=[html.Img(className="logo",
                                                                      src=app.get_asset_url(
                                                                          'nfl-league-logo.png'), ),
                                                             f"NFL Survivor Pool Optimiser", ]),
                                           html.Hr(className="mast_head")]))),
        dbc.Row([
            dbc.Col([
                html.Div(className="side_panel", children=[
                    html.Div(className="subcomponent", children=[
                        html.H3('Enter current league week:', className="side_panel"),
                        dcc.Dropdown(
                            id='current_week',
                            options=[{'label': str(i), 'value': i} for i in weeks],
                            value='',
                            placeholder="Current week",
                            multi=False,
                            className="side_controls"
                        ),
                        html.Br()
                    ]),
                    html.Div(className="subcomponent", children=[
                        html.H3('Optimise through week:', className="side_panel"),
                        dcc.Dropdown(
                            id='target_week',
                            options=[{'label': str(i), 'value': i} for i in target_weeks],
                            value='',
                            placeholder='Final week',
                            multi=False,
                            className="side_controls"
                        ),
                        html.Br()
                    ]),
                    html.Div(className="subcomponent", children=[
                        html.H3('Block Teams:', className="side_panel"),
                        html.Br(),
                        dcc.Dropdown(
                            id='blocked_teams',
                            options=[{'label': get_full_name(i), 'value': i} for i in teams],
                            value='',
                            placeholder='Select Team',
                            multi=True,
                            className="side_controls"
                        ),
                        html.Br()
                    ]),
                ]),
            ]),
            dbc.Col([
                html.Div(className="main_panel", children=[
                    html.Div([
                        #html.Div(id="headline_stats", className="headline_stats"),
                        dcc.Tabs(id="tabs-example", value='probabilities_table', children=[
                            dcc.Tab(label='Team Location', value='team_selector'),
                            dcc.Tab(label='Probabilities Table', value='probabilities_table'),
                            dcc.Tab(label='Projections Graph', value='projections_graph'),
                        ]),
                        html.Div(id='tabs-content-example', className='tab_content')
                    ])
                ]),
            ])
        ]),
        dbc.Row(dbc.Col(html.Div(className="footer",
                                 children=[html.H1("Footer",
                                                   className="footer")]))),
    ])

@app.callback(Output('tabs-content-example', 'children'),
               #Output('headline_stats', 'children')],
              [Input('tabs-example', 'value'),
               Input('current_week', 'value'),
               Input('target_week', 'value'),
               Input('blocked_teams', 'value')])
def render_content(tab, week_start, week_end, blocked_teams):
    if tab == 'team_selector':
        result = get_selector_div(static_df)
    elif tab == 'probabilities_table':
        result = get_table_div(optimizer, week_start, week_end, blocked_teams, thumbnails)
    elif tab == 'projections_graph':
        result = get_projections_graph(static_df=static_df, optimizer=optimizer,week_start=week_start,
                                       week_end=week_end, blocked_teams=blocked_teams)
    return result

if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=8050, debug=True)

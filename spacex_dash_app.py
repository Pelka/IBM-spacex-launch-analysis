# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("./data/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Get Launch Sites of data frame
def get_values(data, name_column):
    return data[name_column].unique()

# Format Launch sites in an array for dropdown menu
def format_sites_dd(data):
    sites = data
    sites = [{
        'label': 'All Sites',
        'value': 'ALL'
    }]

    for site in arr_sites:
        sites.append({'label': site, 'value': site})
    return sites


arr_sites = get_values(spacex_df, 'Launch Site')
arr_booster = get_values(spacex_df, 'Booster Version Category')
dropdown_sites = format_sites_dd(arr_sites)

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(
    children=[
        html.H1(
            'SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36',
                   'font-size': 40}
        ),
        # TASK 1: Add a dropdown list to enable Launch Site selection
        # The default select value is for ALL sites
        html.Br(),
        html.Div(
            dcc.Dropdown(
                id='site-dropdown',
                options=dropdown_sites,
                value='ALL',
                placeholder="place holder here",
                searchable=True
            ),
        ),

        # TASK 2: Add a pie chart to show the total successful launches count for all sites
        # If a specific launch site was selected, show the Success vs. Failed counts for the site
        html.Div(dcc.Graph(id='success-pie-chart')),
        html.Br(),

        html.P("Payload range (Kg):"),
        # TASK 3: Add a slider to select payload range
        # dcc.RangeSlider(id='payload-slider',...)
        html.Div(
            dcc.RangeSlider(
                id='payload-slider',
                min=0, max=10000, step=1000,
                marks={
                    0: '0',
                    2500: '2500',
                    5000: '5000',
                    7500: '7500',
                    10000: '10000'
                },
                value=[min_payload, max_payload]
            )
        ),

        # TASK 4: Add a scatter chart to show the correlation between payload and launch success
        html.Div(
            dcc.Graph(id='success-payload-scatter-chart')
        ),
    ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output

@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    filter_df = spacex_df.loc[spacex_df['Launch Site'] == entered_site]
    filter_df = filter_df.groupby(
        'class')['Launch Site'].count().to_frame().reset_index()    
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class',
                    names='Launch Site',
                    title='Total Succes Launches by Site')
        return fig
    else:
        fig = px.pie(filter_df, values='Launch Site',
                    names='class',
                    title=f'Succes Launches by {entered_site}'
                    )
        return fig
            
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
# Run the app

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value"))

def get_pie_chart(entered_site, selected_mass):
    filter_df = spacex_df.loc[(spacex_df['Payload Mass (kg)'] >= selected_mass[0]) &
                              (spacex_df['Payload Mass (kg)'] <= selected_mass[1])]
    if entered_site == 'ALL':
        fig = px.scatter(
            filter_df,
            x = 'Payload Mass (kg)', 
            y = 'class', 
            color="Booster Version Category"
        )
        return fig
    else:
        filter_df = filter_df.loc[spacex_df['Launch Site'] == entered_site]
        fig = px.scatter(
            filter_df,
            x='Payload Mass (kg)',
            y='class',
            color="Booster Version Category"
        )
        return fig
    
if __name__ == '__main__':
    app.run_server()

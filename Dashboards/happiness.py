from dash import Dash, html, dcc, Input, Output, State
import pandas as pd
import plotly.express as px

happiness = pd.read_csv('data/world_happiness.csv')
app = Dash()
app.layout= html.Div([
    html.H1("World Happiness Dashboard"),
    html.P(['This dashboard shows the happiness score.',
            html.Br(),
            html.A("World Happiness Report Data Source",
                   href="https://worldhappiness.report",
                   target='_blank')]),
    dcc.RadioItems(id='region-radio',
                   options=happiness['region'].unique(),
                   value='North America',
                   inline=True),
    dcc.Dropdown(id="country-dropdown"),
    dcc.RadioItems(id='data-radio', 
                   options={
                       'happiness_score': 'Happiness Score',
                       'happiness_rank': 'Happiness Rank'},
                   value="happiness_score",
                   inline=True),
    html.Br(),
    html.Button(id='submit-button',
                n_clicks=0,
                children='Update the output'),             
    dcc.Graph(id='happiness-graph'),
    html.Div(id='average-div')                  
])

@app.callback(
        Output('country-dropdown','options'),
        Output('country-dropdown','value'),
        Input('region-radio', 'value')
)

def update_dropdown(selected_region):
    filtered_happiness=happiness[happiness['region']==selected_region]
    country_options=filtered_happiness['country'].unique()
    return country_options, country_options[0]

@app.callback(
    Output('happiness-graph', 'figure'),
    Output('average-div','children'),
    Input('submit-button', 'n_clicks'),
    State('country-dropdown', 'value'),
    State('data-radio', 'value')
)

def update_graph(button_click, selected_country, selected_data):
    filtered_happiness=happiness[happiness['country']==selected_country]
    if selected_data=='happiness_score':
        label="Happiness Score"
    else:
        label="Happiness Rank"
    line_fig=px.line(filtered_happiness, x='year', y=selected_data, title=f'{label} in {selected_country}',
                     labels={selected_data: label, 'year': 'Year'})
    selected_average=filtered_happiness[selected_data].mean()
    
    return line_fig, f'The average {label} for {selected_country} is {selected_average}'

if __name__== '__main__':
    app.run(debug=True)
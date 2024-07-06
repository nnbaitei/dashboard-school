import json
import urllib.request
import numpy as np
import plotly.graph_objects as go
from dash import Dash, html, dcc
import pandas as pd
from plotly.subplots import make_subplots
import plotly.express as px
from dash.dependencies import Input, Output

# Function to create bar chart for a given province
def create_bar_chart(province):
    colors = {
    'bg_female': ['#DF007C'],
    'bg_male': ['#FD2D00'] 
    }

    # Read data from CSV
    df = pd.read_csv('student.csv')

    filtered_data = df[df['schools_province'] == province]

    fig = make_subplots(rows=1, cols=1, subplot_titles=[province])

    fig.add_trace(go.Bar(
        x=filtered_data['schools_province'],
        y=filtered_data['totalmale'],
        marker_color=colors['bg_male'],
        text=filtered_data['totalmale'],
        name='Male'
    ), row=1, col=1)

    fig.add_trace(go.Bar(
        x=filtered_data['schools_province'],
        y=filtered_data['totalfemale'],
        marker_color=colors['bg_female'],
        text=filtered_data['totalfemale'],
        name='Female'
    ), row=1, col=1)

    fig.update_traces(textposition='outside', textfont_size=14)  # Place text labels outside the bars

    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        height=500,
        width=700,
        showlegend=True
    )

    return fig

def bar():
    colors = {
        'bg_female': '#DF007C',
        'bg_male': '#00C5C8'
    }
    df = pd.read_csv('student.csv')

    fig = go.Figure()

    # Add male data
    fig.add_trace(go.Bar(
        x=df['schools_province'],
        y=df['totalmale'],
        marker_color=colors['bg_male'],
        text=df['totalmale'],
        name='Male'
    ))

    # Add female data
    fig.add_trace(go.Bar(
        x=df['schools_province'],
        y=df['totalfemale'],
        marker_color=colors['bg_female'],
        text=df['totalfemale'],
        name='Female'
    ))

    # Update layout for combined bar chart
    fig.update_traces(textposition='outside', textfont_size=14)
    fig.update_layout(
        barmode='group',
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        height=700,
        width=1100,
        xaxis_title='Province',
        yaxis_title='Total Students',
        legend_title='Gender',
        showlegend=True,
        bargap=0.2,
    )
    return fig

def map():

    file_path = 'merged_file.json'

    # อ่านไฟล์ JSON
    with open(file_path, 'r', encoding='utf-8') as file:
        jdata = json.load(file)

    fig = go.Figure()

    # Loop through each feature in the geojson file
    for feature in jdata['features']:
        if feature['geometry']['type'] == 'MultiPolygon':
            for polyg in feature['geometry']['coordinates']:
                pts = polyg[0]
                x, y = zip(*pts)
                pro_name = feature['properties']['pro_en']
                pro_name_th = feature['properties']['pro_th']
                male_st = feature['properties']['student']['totalmale']
                female_st = feature['properties']['student']['totalfemale']
                total_st = feature['properties']['student']['totalstd']
                text = f'  {pro_name_th}  <br>  ผู้ชาย: {male_st}  <br>  ผู้หญิง: {female_st}  <br>  รวม: {str(total_st)}  '
                if pro_name == "Songkhla":  # Check if the province is Songkhla
                    fig.add_scatter(x=x, y=y, mode='lines', line_color='#DF007C', line_width=1.5, fill='toself', fillcolor='rgba(255, 0, 0, 0.2)', text=text)
                else:
                    fig.add_scatter(x=x, y=y, mode='lines', line_color='#999999', line_width=1.5, fill='toself', fillcolor='rgba(200, 200, 200, 0.2)', text=text)

    fig.update_layout(width=600, 
                    height=1000, 
                    xaxis_showgrid=False, 
                    yaxis_showgrid=False, 
                    showlegend=False, 
                    template='plotly_dark',
                    plot_bgcolor='rgba(0, 0, 0, 0)',
                    paper_bgcolor='rgba(0, 0, 0, 0)',
                    )
                    
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    return fig

colors = {
    'background': '#1D1B26',
    'text': '#FFFFFF'
    }
    
fig_map = map()
fig_bar = bar()

# List of provinces
df = pd.read_csv('student.csv')
provinces = df['schools_province'].unique()
default_province = 'สงขลา'

app = Dash(__name__)
app.layout = html.Div(children=[
    html.H1(
        'Information about students graduating in 2024',
        className='gradient-text' 
    ),

    # html.Div(children='สถิตินักเรียนจบการศึกษา ปี 2567: แสดงตามเพศและจังหวัด', style={
    #     'textAlign': 'center',
    #     'color': colors['text'],
    #     'opacity': 0.6,
    #     'font-size': "24px"
    # },),
    html.Div(
        children=[
            html.Div(
                [
                    html.Div(dcc.Graph(id='example-graph-1', figure=fig_map)
                            #  className='six columns',
                            #  style={'width': '0px'}
                            ),
                    html.Div(
                        [
                            html.Div([
                                html.Label('Select Province', style={'font-size': '40px', 'font-weight': 'semi-bold', 'margin-bottom': '20px', 'color': colors['text'], 'opacity': 0.6,}),
                                dcc.Dropdown(
                                    id='province-dropdown',
                                    options=[{'label': province, 'value': province} for province in provinces],
                                    value=default_province  # Default value
                                ),
                                html.Div(
                                    [
                                    dcc.Graph(id='province-graph', figure=create_bar_chart(default_province), style={'margin': 'auto'})
                                    ], style={'display':'flex','justifyContent': 'center', 'alignItems': 'center'}
                                )
                            ], style={'paddingTop': '60px'}),

                            html.Label('Overview', style={'font-size': '40px', 'font-weight': 'semi-bold', 'color': colors['text'], 'opacity': 0.6,}), 

                            html.Div(
                                dcc.Graph(id='example-graph-1', figure=fig_bar),
                                style={'height':'500px', 'width': 'auto'}
                            )
                        ],
                        style={'display': 'flex', 'flexDirection': 'column', 'gap':'50px'}         
                    )
                ],
                style={'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'center', 'alignItems': 'center'}
                # style={'backgroundColor': '#ffffff'}
            )
        ]
    )
])


# Callback to update graph based on selected province
@app.callback(
    Output('province-graph', 'figure'),
    [Input('province-dropdown', 'value')]
)
def update_graph(selected_province):
    return create_bar_chart(selected_province)

if __name__ == '__main__':
    app.run(debug=True)

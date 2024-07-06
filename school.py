import json
import urllib.request
import numpy as np
import plotly.graph_objects as go
from dash import Dash, html, dcc

# Load and read the geojson file for Thailand regions.
# thai_url = "https://raw.githubusercontent.com/chingchai/OpenGISData-Thailand/master/provinces.geojson"
# with urllib.request.urlopen(thai_url) as url:
#     jdata = json.loads(url.read().decode())

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
                    fig.add_scatter(x=x, y=y, mode='lines', line_color='red', line_width=1.5, fill='toself', fillcolor='rgba(255, 0, 0, 0.2)', text=text)
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

if __name__ == '__main__':

    colors = {
    'background': '#1D1B26',
    'text': '#FFFFFF'
    }
    

    fig_map = map()
    app = Dash()
    app.layout = html.Div(children=[
        html.H1(
            'Information about students graduating in 2024',
            className='gradient-text' 
        ),

        html.Div(children='สถิตินักเรียนจบการศึกษา ปี 2567: แสดงตามเพศและจังหวัด', style={
            'textAlign': 'center',
            'color': colors['text'],
            'opacity': 0.6,
            'font-size': "24px"
        },),
        html.Div(
            dcc.Graph(id='example-graph',
                  figure=fig_map,
                  )
        )
        
    ])
    app.run_server()

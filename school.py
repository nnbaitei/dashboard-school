import json
import urllib.request
import numpy as np
import plotly.graph_objects as go
from dash import Dash, html, dcc
import pandas as pd
from plotly.subplots import make_subplots
import plotly.express as px

# Load and read the geojson file for Thailand regions.
# thai_url = "https://raw.githubusercontent.com/chingchai/OpenGISData-Thailand/master/provinces.geojson"
# with urllib.request.urlopen(thai_url) as url:
#     jdata = json.loads(url.read().decode())

def bar():
    df = pd.read_csv('student.csv')

    # สร้างลิสต์ของจังหวัดที่มีอยู่ในคอลัมน์ 'schools_province'
    provinces = df['schools_province'].unique()

    # กรองข้อมูลเฉพาะจังหวัดที่มีในลิสต์ provinces
    df_filtered = df[df['schools_province'].isin(provinces)]

    # คำนวณจำนวนแถวที่เหมาะสมต่อคอลัมน์ (หากไม่แน่ใจถึงจำนวนจะใช้)
    num_rows = (len(provinces) + 3) // 4  # จำนวนแถวที่เหมาะสมต่อคอลัมน์ (4 แถว)

    # สร้างกราฟบาร์โดยใช้ Plotly Express ทั้งหมดใน DataFrame ที่กรองแล้ว
    fig = make_subplots(rows=num_rows, cols=4, subplot_titles=provinces)

    # เพิ่มกราฟบาร์แต่ละจังหวัดเป็น subplot
    for i, province in enumerate(provinces):
        row = i // 4 + 1  # หาแถวที่เหมาะสมสำหรับ subplot
        col = i % 4 + 1   # หาคอลัมน์ที่เหมาะสมสำหรับ subplot
        filtered_data = df_filtered[df_filtered['schools_province'] == province]

        # เพิ่มกราฟบาร์ชายและหญิง
        fig.add_trace(px.bar(data_frame=filtered_data, x='schools_province', y='totalmale', 
                            barmode='group', color_discrete_sequence=['blue'], text='totalmale').data[0], 
                    row=row, col=col)

        fig.add_trace(px.bar(data_frame=filtered_data, x='schools_province', y='totalfemale', 
                            barmode='group', color_discrete_sequence=['red'], text='totalfemale').data[0], 
                    row=row, col=col)
    # กำหนดเลเยอร์และรายละเอียด
    fig.update_layout(
                    
                    template='plotly_dark',
                    plot_bgcolor='rgba(0, 0, 0, 0)',
                    paper_bgcolor='rgba(0, 0, 0, 0)',
                    height=9000,
                    width=1000
                    )  # ปรับความสูงของกราฟเพื่อให้มองได้ชัดเจน
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
    fig_bar = bar()
    
    app = Dash(__name__)
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
            children=[
                html.Div(
                    [
                        html.Div(dcc.Graph(id='example-graph-1', figure=fig_map)
                                #  className='six columns',
                                #  style={'width': '0px'}
                                ),
                        html.Div(dcc.Graph(id='example-graph-2', figure=fig_bar),
                                #  className='six columns',
                                 style={'height':'500px', 'width': 'auto', 'overflow-y':'scroll', 'display':'flex', 'justifyContent': 'flex-end'}
                                )
                    ],
                    style={'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'center', 'alignItems': 'center'}
                    # style={'backgroundColor': '#ffffff'}
                )
            ]
)
        
    ])
    app.run(debug=True)

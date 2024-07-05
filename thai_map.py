import json
import urllib.request
import numpy as np
import plotly.graph_objects as go
from dash import Dash, html, dcc

# Load and read the geojson file for Thailand regions.
thai_url = "https://raw.githubusercontent.com/chingchai/OpenGISData-Thailand/master/provinces.geojson"
with urllib.request.urlopen(thai_url) as url:
    jdata = json.loads(url.read().decode())

fig = go.Figure()

# Loop through each feature in the geojson file
for feature in jdata['features']:
    if feature['geometry']['type'] == 'MultiPolygon':
        for polyg in feature['geometry']['coordinates']:
            pts = polyg[0]
            x, y = zip(*pts)
            pro_name = feature['properties']['pro_en']
            if pro_name == "Songkhla":  # Check if the province is Songkhla
                fig.add_scatter(x=x, y=y, mode='lines', line_color='red', line_width=1.5, fill='toself', fillcolor='rgba(255, 0, 0, 0.2)', text=pro_name)
            else:
                fig.add_scatter(x=x, y=y, mode='lines', line_color='#999999', line_width=1.5, fill='toself', fillcolor='rgba(200, 200, 200, 0.2)', text=pro_name)

fig.update_layout(width=600, 
                  height=900, 
                  xaxis_showgrid=False, 
                  yaxis_showgrid=False, 
                  showlegend=False, 
                  template='plotly_dark',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  paper_bgcolor='rgba(0, 0, 0, 0)')
fig.update_xaxes(showticklabels=False)
fig.update_yaxes(showticklabels=False)

app = Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run_server()

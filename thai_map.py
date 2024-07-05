import json
import urllib.request
import numpy as np
import plotly.graph_objects as go
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash import Dash, html, dcc, Output, Input
from dash_extensions.javascript import assign


#Load and read the geojson file for Thailand regions. 
italy_url = "https://raw.githubusercontent.com/chingchai/OpenGISData-Thailand/master/provinces.geojson"
with urllib.request.urlopen(italy_url) as url:
        jdata = json.loads(url.read().decode())
              
pts = []#list of points defining boundaries of polygons
for  feature in jdata['features']:
    if feature['geometry']['type'] == 'Polygon':
        pts.extend(feature['geometry']['coordinates'][0])    
        pts.append([None, None])#mark the end of a polygon   
        
    elif feature['geometry']['type'] == 'MultiPolygon':
        for polyg in feature['geometry']['coordinates']:
            pts.extend(polyg[0])
            pts.append([None, None])#end of polygon
    elif feature['geometry']['type'] == 'LineString': 
        pts.extend(feature['geometry']['coordinates'])
        pts.append([None, None])
    else: pass           
    #else: raise ValueError("geometry type irrelevant for map")

x, y = zip(*pts)    

fig = go.Figure()
fig.add_scatter(x=x, y=y, mode='lines', line_color='#999999', line_width=1.5)
fig.update_layout(width=600,  height=800)

app = Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])


if __name__ == '__main__':
    app.run_server()
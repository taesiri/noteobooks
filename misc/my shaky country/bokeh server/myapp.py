from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc
from bokeh.models import (
  GMapPlot, GMapOptions, ColumnDataSource, Circle, Range1d, PanTool, WheelZoomTool, BoxSelectTool, Button, ColumnDataSource, CustomJS
)
from bokeh.layouts import row, widgetbox, column
from bokeh.models.widgets import RangeSlider, DataTable, TableColumn, NumberFormatter
from bokeh.io import curdoc

import xml.etree.ElementTree as ElementTree
import pandas as pd
import requests
import os.path

contents = None
plot = None

try:
    print("Fetching latest data!")
    r = requests.get('http://irsc.ut.ac.ir/events_list.xml', timeout=3)
    if r.status_code == 200:
        with open('latest.xml', 'wb') as f:
            f.write(r.content)
except requests.exceptions.Timeout:
    print('timeout!')

if os.path.isfile('latest.xml'):
    with open('latest.xml', 'rb') as f:
        contents = f.read()


if contents:
    root = ElementTree.fromstring(contents)

    all_records = []
    for i, child in enumerate(root):
        record = {}
        for subchild in child:
            record[subchild.tag] = subchild.text
        all_records.append(record)

    df = pd.DataFrame(all_records)
    df['date'] = df['date'].astype('datetime64[ns]')

    lats = df['lat'].apply(lambda x: x.split(' ')[0])
    longs = df['long'].apply(lambda x: x.split(' ')[0])


    map_options = GMapOptions(lat=35.68, lng=50.95, map_type="roadmap", zoom=10)

    plot = GMapPlot(x_range=Range1d(), y_range=Range1d(), map_options=map_options)
    plot.title.text = "Iran"
    plot.api_key = "API_KEY"

    source = ColumnDataSource(
        data=dict(
            lat=lats,
            lon=longs,
        )
    )

    circle = Circle(x="lon", y="lat", size=10, fill_color="red", fill_alpha=0.8, line_color=None)
    plot.add_glyph(source, circle)

    plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool())

    plot.width = 1280
    plot.height = 720
else:
    plot = figure()

source = ColumnDataSource(data=dict())

def update():
    source.data = {
        'id'    : df.id,
        'date'  : df.date,
        'dep'   : df.dep,
        'lat'   : df.lat,
        'long'  : df.long,
        'mag'   : df.mag,
        'reg1'  : df.reg1,
        'reg2'  : df.reg2,
        'reg3'  : df.reg3
    }

columns = [
    TableColumn(field="id", title="id", width=55),
    TableColumn(field="date", title="date"),
    TableColumn(field="dep", title="depth", width=35),
    TableColumn(field="lat", title="lat", width=55),
    TableColumn(field="long", title="long", width=55),
    TableColumn(field="mag", title="magnitude", width=55),
    TableColumn(field="reg1", title="reg1"),
    TableColumn(field="reg2", title="reg2"),
    TableColumn(field="reg3", title="reg3") 
]

data_table = DataTable(source=source, columns=columns, width=1280)
table = widgetbox(data_table)

curdoc().add_root(column(plot, table))
curdoc().title = "Earth Shaking ..."

update()

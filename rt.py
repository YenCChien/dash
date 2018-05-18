import dash
from dash.dependencies import Output, Event
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
import sqlite3
import pandas as pd


app = dash.Dash(__name__)
app.layout = html.Div(
    [
        dcc.Graph(
            id='live-graph', 
            animate=True,
        ),
        dcc.Interval(
            id='graph-update',
            interval=1*1000,
        )
    ]
)

@app.callback(Output('live-graph', 'figure'),
              events=[Event('graph-update', 'interval')])
def update_graph_scatter():
    # X.append(X[-1]+1)
    # Y.append(Y[-1]+1)
    # try:
    title = 'HTMN4-UNE'
    conn = sqlite3.connect('HTMN4-UNE')
    c = conn.cursor()
    getlist = conn.execute("SELECT * FROM sqlite_master where type='table'")
    tablelist,tb = [],[]
    for list in getlist:
        tablelist.append(list)
    for x in tablelist:
        tb.append(x[1])
    datalist = []
    for table in tb:
        # conn.execute("SELECT COUNT(*) FROM (SELECT `_rowid_`,* FROM `{}` ORDER BY `Frequency` DESC)".format(table))
        # conn.execute("SELECT `_rowid_`,* FROM `{}` ORDER BY `Frequency` DESC LIMIT 0, 50000".format(table))
        # conn.execute("SELECT COUNT(*) FROM (SELECT `_rowid_`,* FROM `{}` ORDER BY `Frequency` ASC)".format(table))
        # conn.execute("SELECT `_rowid_`,* FROM `{}` ORDER BY `Frequency` ASC LIMIT 0, 50000".format(table))
        df = pd.read_sql("SELECT * FROM `{}` ORDER BY `_rowid_` ASC LIMIT 0, 50000".format(table), conn)
        X = df['Frequency']
        Y = df['REPORT']
        data = plotly.graph_objs.Scatter(
                x=X,
                y=Y,
                name=table,
                mode= 'lines+markers'
                )
        datalist.append(data)
    return {'data': datalist, 'layout':go.Layout(title=title)}
    # except Exception as e:
        # with open('errors.txt','a') as f:
            # f.write(str(e))
            # f.write('\n')

if __name__ == '__main__':
    app.run_server(debug=True)
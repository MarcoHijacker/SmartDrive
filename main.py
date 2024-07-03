import dash
from dash.dependencies import Output, Input
from dash import dcc, html
from datetime import datetime
import json
import plotly.graph_objs as go
from collections import deque
from flask import Flask, request
from pymongo import MongoClient

server = Flask(__name__)
app = dash.Dash(__name__, server=server)

MAX_DATA_POINTS = 1000
UPDATE_FREQ_MS = 100

time = deque(maxlen=MAX_DATA_POINTS)
accel_x = deque(maxlen=MAX_DATA_POINTS)
accel_y = deque(maxlen=MAX_DATA_POINTS)
accel_z = deque(maxlen=MAX_DATA_POINTS)
gyro_x = deque(maxlen=MAX_DATA_POINTS)
gyro_y = deque(maxlen=MAX_DATA_POINTS)
gyro_z = deque(maxlen=MAX_DATA_POINTS)
latitude = deque(maxlen=MAX_DATA_POINTS)
longitude = deque(maxlen=MAX_DATA_POINTS)

app.layout = html.Div(
    [
        dcc.Markdown(
            children="""
            # Live Sensor Readings
            Streamed from Sensor Logger: tszheichoi.com/sensorlogger
        """
        ),
        dcc.Graph(id="live_graph"),
        dcc.Interval(id="counter", interval=UPDATE_FREQ_MS),
    ]
)


@app.callback(Output("live_graph", "figure"), Input("counter", "n_intervals"))
def update_graph(_counter):
 """

    data = [
        go.Scatter(x=list(time), y=list(d), name=name)
        for d, name in zip(
            [accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z],
            ["Accel X", "Accel Y", "Accel Z", "Gyro X", "Gyro Y", "Gyro Z"]
        )
    ]

    graph = {
        "data": data,
        "layout": go.Layout(
            {
                "xaxis": {"type": "date"},
                "yaxis": {"title": "Acceleration and Gyro readings"},
            }
        ),
    }
    if len(time) > 0:  # cannot adjust plot ranges until there is at least one data point
        graph["layout"]["xaxis"]["range"] = [min(time), max(time)]
        graph["layout"]["yaxis"]["range"] = [
            min(accel_x + accel_y + accel_z + gyro_x + gyro_y + gyro_z),
            max(accel_x + accel_y + accel_z + gyro_x + gyro_y + gyro_z),
        ]

    return graph
 """



client = MongoClient('mongodb://localhost:27017/')
db = client['sensor_data']
collection = db['readings']


@server.route("/data", methods=["POST"])
def data():  # listens to the data streamed from the sensor logger
    if str(request.method) == "POST":
        #print(f'received data: {request.data}')
        data = json.loads(request.data)
        for d in data['payload']:
            ts = datetime.fromtimestamp(d["time"] / 1000000000)
            if len(time) == 0 or ts > time[-1]:
                time.append(ts)
                doc = {"time": ts}
                #if d.get("name", None) == "accelerometer" and d.get("name", None) == "gyroscope":
                accel_x.append(d["values"]["x"])
                accel_y.append(d["values"]["y"])
                accel_z.append(d["values"]["z"])
                gyro_x.append(d["values"]["x"])
                gyro_y.append(d["values"]["y"])
                gyro_z.append(d["values"]["z"])
                latitude.append(d["values"]["latitude"])
                longitude.append(d["values"]["longitude"])

                doc.update({
                    "accel_x": d["values"]["x"],
                    "accel_y": d["values"]["y"],
                    "accel_z": d["values"]["z"],
                    "gyro_x": d["values"]["x"],
                    "gyro_y": d["values"]["y"],
                    "gyro_z": d["values"]["z"],
                    "latitude": d["values"]["latitude"],
                    "longitude": d["values"]["longitude"]
                })
                collection.insert_one(doc)
                #print(f"Accelerometer - x: {d['values']['x']}, y: {d['values']['y']}, z: {d['values']['z']}")
                time.sleep(1.0)
    return "success"


if __name__ == "__main__":
    app.run_server(port=8000, host="0.0.0.0")

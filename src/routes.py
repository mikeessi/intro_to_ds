from flask import render_template
import json
from src import app


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/statistics")
def statistics():
    return render_template("statistics.html")

@app.route("/predictions")
def predictions():
    data = read_predictions()
    return render_template("predictions.html", data=data)

def read_predictions():
    rows = []
    with open("predictions.json") as file:
        for line in file:
            d = json.loads(line)
            rows.append(d)
    data = [row for row in rows if row["Vuosi"] == 2025]
    return data
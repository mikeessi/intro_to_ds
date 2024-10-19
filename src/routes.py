from flask import render_template
from src import app


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/statistics")
def statistics():
    return render_template("statistics.html")

@app.route("/predictions")
def predictions():
    return render_template("predictions.html")
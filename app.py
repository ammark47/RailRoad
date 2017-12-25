from flask import Flask,render_template,request, url_for, redirect
from models.models import *

app = Flask(__name__)

@app.route("/")
def main():
    available_stations = get_stations()
    return render_template('home.html', stations = available_stations)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=True)

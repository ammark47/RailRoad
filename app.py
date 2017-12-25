from flask import Flask,render_template,request, url_for, redirect
from models.models import *

app = Flask(__name__)

@app.route("/")
def main():
    available_stations = get_stations()
    return render_template('home.html', stations = available_stations)

@app.route('/search-trains',methods=["POST"])
def search_trains():
    if request.method == "POST":
        dep_date = request.form['departure-date']
        dep_time = request.form['departure-time']
        outgoing_station = request.form['from-station']
        destination_station = request.form['to-station']

    




if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=True)

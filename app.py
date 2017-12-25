from flask import Flask,render_template,request, url_for, redirect
from models.models import *

app = Flask(__name__)

@app.route("/")
def main():
    available_stations = get_stations()
    return render_template('home.html', stations = available_stations)

@app.route('/search-trains', methods=["POST"])
def search_trains():
    if request.method == "POST":
        dep_date = request.form['departure-date']
        outgoing_station = request.form['from-station']
        destination_station = request.form['to-station']

        results = []
        trips = []

        trips.append(get_available_trains(dep_date,outgoing_station,destination_station))

        if results:
            for x in range(len(results[0])):
                results.append(result(results[0][x][0],_dep_date, results[0][x][2],_outgoing_station, _destination_station))

        return render_template('train_options.html', results = results)

@app.route('/purchase', methods =['POST'])
def purchase():
    if request.method == 'POST':
        result_id = request.form['book_button']  # result type - still need to be defined

        print(result_id)

        #if result_id
        #page that has the form- once form is submitted - goes to purchase act
        return render_template('purchase.html', result = result_id)


class result:
    def __init__(self,train_num,dep_date,outgoing_station,destination_station):
        self.train_id = train_num
        self.dep_date = dep_date
        self.outgoing_station = get_destination_stations(outgoing_station,destination_station)[0]
        self.destination_station = get_destination_stations(outgoing_station,destination_station)[1]




if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=True)

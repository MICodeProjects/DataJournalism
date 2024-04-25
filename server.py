from flask import Flask
from flask import request
from flask import render_template
import json
app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/about.html')
def about():
    #load a current view of the data
    total=0
    f = open("data/traffic_crashes.json", "r")
    data = json.load(f)
    f.close()
   
    #render the template with the apporpriate data
    return render_template('about.html', data=data)


@app.route('/accidentmap.html')
def accidentmap():
    #load a current view of the data
    f = open("data/traffic_crashes.json", "r")
    data = json.load(f)
    f.close()


    return render_template('accidentmap.html', data=data)

@app.route('/speedlimits.html')
def speedlimits():
    #load a current view of the data
    f = open("data/traffic_crashes.json", "r")
    data = json.load(f)
    f.close()


    return render_template('speedlimits.html', data=data)



@app.route('/trafficcontrols.html')
def trafficcontrols():
    #load a current view of the data
    f = open("data/traffic_crashes.json", "r")
    data = json.load(f)
    f.close()


    return render_template('trafficcontrols.html', data=data)

app.run(debug=True)
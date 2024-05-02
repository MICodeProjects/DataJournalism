from flask import Flask
from flask import request
from flask import render_template
import json
import math
app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def index():
    #load a current view of the data
    total=0
    f = open("data/traffic_crashes.json", "r")
    data = json.load(f)
    f.close()

    #render the template with the apporpriate data
    return render_template('index.html', data=data)

@app.route('/accidentmap')
def accidentmap():
    #load a current view of the data
    f = open("data/traffic_crashes.json", "r")
    data = json.load(f)
    f.close()
# top left = 42.055459, -87.940923
# bottom right = 41.640921, -87.524904
# viewbox = "0 0 1861.5 2529.5"
    top_left = (42.055459, -87.940923)
    bottom_right = (41.640921, -87.524904)
    viewbox = ((0, 0), (1861.5, 2529.5))
    viewbox_width = viewbox[1][0]-viewbox[0][0]
    viewbox_length = viewbox[1][1]-viewbox[0][1]
    coords_width = top_left[0] - bottom_right[0]
    coords_length = top_left[1] - bottom_right[1]

    # changing all of the real life coordinates to svg coordinates....hope it works
    for crash in data.keys():
        og_lat = data[crash]["latitude"] # saving original latitude and longitude values
        og_log = data[crash]["longitude"]

        data[crash]["latitude"] = viewbox[0][0] + (viewbox_width/coords_width)*og_lat # latitude is horizontal x, longitude is vertical y
        data[crash]["longitude"] = viewbox[0][1] + (viewbox_length/coords_length)*og_log # latitude is horizontal x, longitude is vertical y

    #Filter and reformat data for ease of access in the template

    return render_template('accidentmap.html', data=data)


@app.route('/graph/<graph_type>')
def graph(graph_type):
    #load a current view of the data
    f = open("data/traffic_crashes.json", "r")
    data = json.load(f)
    f.close()

    
    #Filter and reformat data for ease of access in the template
    data_length = len(data)
    piechart_data = {}
    barchart_data = {}
    for crash in data.keys():
        val = data[crash][graph_type]

        # pie chart data sorting. If that type is not in the list, add it. Otherwise, add a tick. (out of total)
        if val not in piechart_data:
            piechart_data[val] = 1
        else:
            piechart_data[val] +=1
        
        # barchart data sorting. Average injuries on y axis, so x axis has val
        if val not in barchart_data:
            barchart_data[val] = data[crash]["injuries_total"]
        else:
            barchart_data[val]+=data[crash]["injuries_total"]
    
    # turn pie chart data into percents, then sort by biggest to smallest.
    for crash in piechart_data:
        piechart_data[crash] = round((piechart_data[crash]/data_length)*100)
    piechart_data_list = [(k, v) for k, v in piechart_data.items()]
    piechart_data_list.sort()
    
    # get average injuries in barchart data
    for crash in barchart_data:
        barchart_data[crash] = barchart_data[crash]/data_length
    barchart_data_list = [(k, v) for k, v in barchart_data.items()]
    barchart_data_list.sort()
    
    print(barchart_data_list)
    print(piechart_data)
   
    return render_template('graph.html', data=data, barchart_data=barchart_data_list, title=graph_type, piechart_data=piechart_data)


app.run(debug=True)
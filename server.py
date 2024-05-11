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
# top left = 42.06635892943516, -87.9373044183777
# bottom right = 41°38'15.2"N 87°31'31.2"W or 
    #41.63770533897127, -87.52532536441811
# viewbox = "0 0 1861.5 2529.5"
    left =-87.938165 #-87.9373044183777
    right=-87.52573 #-87.52532536441811
    top=42.056015 #42.06635892943516
    down=41.639689 #41.63770533897127
    viewbox = (1861.5, 2529.5)
    coords_width = left-right
    coords_length = top-down
    width_pixel = coords_width/viewbox[0] # a single pixel is this many degrees
    length_pixel = coords_length/viewbox[1] # how many degrees per pixel
    print(width_pixel,length_pixel)
    # changing all of the real life coordinates to svg coordinates....hope it works
    for crash in data.keys():
        og_lat = data[crash]["latitude"] # saving original latitude and longitude values
        og_log = data[crash]["longitude"]        
        data[crash]["latitude"] = (top-og_lat)/length_pixel # latitude is y, longitude is vertical x
        data[crash]["longitude"] = (left-og_log)/width_pixel 
        print(data[crash]["longitude"], data[crash]["latitude"])
        data[crash]["injuries_total"]
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
    piechart_data_list = {}
    barchart_data = {}
    totals={}
    print(graph_type)
    pie_total = 0
    for crash in data.keys():
        val = data[crash][graph_type]

        # barchart data sorting. Average injuries on y axis, so x axis has val
        if val not in totals:
            totals[val] = 1
            barchart_data[val] = data[crash]["injuries_total"]
        else:
            totals[val] +=1
            barchart_data[val]+=data[crash]["injuries_total"]
    
    # turn pie chart data into percents, then sort by biggest to smallest.
    if "Other" in totals.keys():
        del totals["Other"]
    for type in totals:
        i = totals[type]
        if 100*i/data_length >=2:
            piechart_data_list[type] = round(100*i/data_length,1)
        else:
            if "Other" in piechart_data_list.keys():
                piechart_data_list["Other"]+=100*totals[type]/data_length,1
            else:
                piechart_data_list["Other"]=100*totals[type]/data_length,1
            

    piechart_data_list = [(k, v) for k, v in piechart_data_list.items()] # k is crash type, v is value
    
    # sorting from biggest to smallest
    for i in range(len(piechart_data_list)-1):
    
        # Find the minimum element in remaining 
        # unsorted array
        min_idx = i
        for j in range(i+1, len(piechart_data_list)):
            if piechart_data_list[min_idx][1] > piechart_data_list[j][1]:
                min_idx = j
                
        # Swap the found minimum element with 
        # the first element        
        piechart_data_list[i], piechart_data_list[min_idx] = piechart_data_list[min_idx], piechart_data_list[i]
        
    
    piechart_data_list=piechart_data_list[::-1]
    toadd=0
    piechart_vals=[]
    for val in piechart_data_list:
        toadd+=val[1]
        piechart_vals.append(toadd)
    
    # get average injuries in barchart data
    for crash in barchart_data:
        barchart_data[crash] = round(barchart_data[crash]/totals[crash],1)
    barchart_data_list = [(k, v) for k, v in barchart_data.items()]

    # sorting from biggest to smallest
    for i in range(len(barchart_data_list)-1):
    
        # Find the minimum element in remaining 
        # unsorted array
        min_idx = i
        for j in range(i+1, len(barchart_data_list)):
            if barchart_data_list[min_idx][1] > barchart_data_list[j][1]:
                min_idx = j
                
        # Swap the found minimum element with 
        # the first element        
        barchart_data_list[i], barchart_data_list[min_idx] = barchart_data_list[min_idx], barchart_data_list[i]
    barchart_data_list = barchart_data_list[::-1]

    print(barchart_data_list)
    print(piechart_data_list)
    print(piechart_vals)
    piechart_vals[-1] = 100
    
    return render_template('graph.html', piechart_len=len(piechart_data_list), barchart_len=1500,piechart_vals=piechart_vals, data=data, barchart_data=barchart_data_list, title=graph_type, piechart_data=piechart_data_list)


app.run(debug=True)
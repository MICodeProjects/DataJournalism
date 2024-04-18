import json

f= open("data/traffic_crashes2.csv", "r")

lines = f.readlines()
dict1 = {}

for line in lines:
    line = line.split(",")


    dict1[line[0]] = {"speed_limit":line[1], "control_dev":line[2], "dev_condition":line[3], "way_type":line[4],"intersect_related":line[5],"cause":line[6],"street_name":line[7],"total_injuries":line[8],"latitude":line[9],"longitude":line[10]}



f.close()

#Save the json object to a file
f2 = open("data/traffic_crashes.json", "w")
json.dump(dict1, f2, indent = 4)

f2.close()
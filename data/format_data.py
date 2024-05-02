import json

f= open("data/TrafficCrashes3.csv", "r")

lines = f.readlines()
dict1 = {}

for line in lines[1::]:
    line = line.split(",")


    dict1[line[0]] = {"Speed Limit":int(line[1]), "Presence of Traffic Control Device":line[2], "Weather Conditions":line[3], "Road Lighting":line[4],"Road Type":line[6],"Intersection Related":line[8],"cause":line[9], "injuries_total":int(line[11]),"injuries_fatal":int(line[12]),"latitude":float(line[14]),"longitude":float(line[15])}
# 0 CRASH_DATE, 1 POSTED_SPEED_LIMIT, 2 TRAFFIC_CONTROL_DEVICE, 3 DEVICE_CONDITION,4 TRAFFICWAY_TYPE,5 INTERSECTION_RELATED_I,
# 6 PRIM_CONTRIBUTORY_CAUSE, 7 STREET_NAME,8 INJURIES_TOTAL,9 LATITUDE,10 LONGITUDE
    
# CRASH_DATE,POSTED_SPEED_LIMIT,TRAFFIC_CONTROL_DEVICE,WEATHER_CONDITION,LIGHTING_CONDITION,FIRST_CRASH_TYPE,TRAFFICWAY_TYPE,
# ALIGNMENT,INTERSECTION_RELATED_I,PRIM_CONTRIBUTORY_CAUSE,STREET_NAME,INJURIES_TOTAL,INJURIES_FATAL,INJURIES_INCAPACITATING,LATITUDE,LONGITUDE





f.close()

#Save the json object to a file
f2 = open("data/traffic_crashes.json", "w")
json.dump(dict1, f2, indent = 4)

f2.close()
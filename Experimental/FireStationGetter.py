import overpy
import time
import csv

api = overpy.Overpass()
limit=0

# fetch all nodes where the natural tag is equal to "wood"
result = api.query("""node(32.332755, -124.777692, 44.161841, -113.942646)["amenity"="fire_station"];out body;""")

with open('fire_Station_locations.csv', 'wt') as csv_file:
    writer=csv.writer(csv_file)
    for node in result.nodes:
    
        #Get coordinates for each forest.
        writer.writerow([node.lat, node.lon])
        #Making sure you don't break the maximum number of requests that can be made per minute.
        limit+=1
        print(limit)
        if limit==700:
            time.sleep(60)

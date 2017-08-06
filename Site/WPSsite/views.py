import csv
import os
from django.shortcuts import render
from django import template
def index(request):
    return render(request, 'WPSsite/index.html')

def app(request):
    my_dict = {}
    station = []
    longs = []
    reader = csv.reader(open(os.path.dirname(os.path.realpath(__file__)) + '/svmoutput.csv','r'))
    stations = csv.reader(open(os.path.dirname(os.path.realpath(__file__)) + '/firestations.csv','r'))

    for row in stations:
        station.append(row)

    #ADD IN LOGIC TO INCLUDE LOCATIONS HERE
    counter = 0
    for row in reader:
        if row[0] == "":
            pass
        else:
            key = []
            key.append("{0:.4f}".format(float(row[2])))
            key.append("{0:.4f}".format(float(row[3])))
            
            perc = float(row[11])

            if repr(key) in my_dict:
                my_dict[repr(key)].append(perc)
            else:
                my_dict[repr(key)] = [station[counter]]
                my_dict[repr(key)].append(perc)
                counter = counter + 1
                
    return render(request, 'WPSsite/app.html', {'my_dict':my_dict})




def outreach(request):
    print("hello")
    return render(request, 'WPSsite/outreach.html')

def docs(request):
    return render(request, 'WPSsite/docs.html')

def mission(request):
    return render(request, 'WPSsite/mission.html')

def team(request):
    return render(request, 'WPSsite/team.html')

def contact(request):
    return render(request, 'WPSsite/contact.html')

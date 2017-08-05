'''
Author: Vishal Soomaney

@License: MIT, See License.txt at root of project. 

This script is called everyday by the server. It calls the relevant scripts to get new model predictions
'''


from datetime import datetime
from threading import Timer
import dark_sky as darksky #Location weather information
import MakePrediction as MakePrediction #object that can be used to communicate with model.

file='forest_locations.csv'
key = 'e5d530b79eb4c2232e41a7ab30a208e4'

weatherGetter = darksky.Weather_data(file,key, 193) #instantiate  weather prediction object
makePrediction= MakePrediction.MakePrediction()

def call_daily():

    x=datetime.today()
    y=x.replace(day=x.day+1, hour=1, minute=0, second=0, microsecond=0)
    delta_t=y-x
    secs=delta_t.seconds

    #weatherGetter.produce_Output("initial")
    weatherGetter.produce_Output("add1")
    print("1 day of data added")
    weatherGetter.produce_final()
    print("14 day averages updated")
    weatherGetter.produce_Output("future")
    print("Future forecast obtained")
    weatherGetter.output_to_svm()
    print("SVM input updated")
    makePrediction.prediction() # activate model prediction protocol
    print("SVM output updated/created")
    t=Timer(secs, call_daily)
    t.start()

call_daily()

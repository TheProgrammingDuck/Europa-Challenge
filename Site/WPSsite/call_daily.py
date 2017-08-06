import datetime
from threading import Timer
import dark_sky as darksky
import MakePrediction as MakePrediction
import schedule
import time

file='forest_locations.csv'
key = 'e5d530b79eb4c2232e41a7ab30a208e4'

weatherGetter = darksky.Weather_data(file,key, 210)
makePrediction= MakePrediction.MakePrediction()

def call_daily():

    weatherGetter.produce_Output("add1")
    print("1 day of data added")
    weatherGetter.produce_final()
    print("14 day averages updated")
    weatherGetter.produce_Output("future")
    print("Future forecast obtained")
    weatherGetter.output_to_svm()
    print("SVM input updated")
    makePrediction.prediction()
    print("SVM output updated/created")


schedule.every().day.at("01:00").do(call_daily)
while True:
    schedule.run_pending()
    time.sleep(1)
    

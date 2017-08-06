import datetime
from threading import Timer
import dark_sky as darksky
import MakePrediction as MakePrediction
import schedule
import time

"""The url for the csv containing forest locations and our Dark Sky key.
Dark Sky key has been removed so that it cannot be copied and used by another"""

file='forest_locations.csv'
key = ''

"""Initialising once, all scripts have been optimised so that they don't 
have to be reinitialised to handle updated data"""
weatherGetter = darksky.Weather_data(file,key, 210)
makePrediction= MakePrediction.MakePrediction()

def call_daily():

    """Updating everything in the right order, the output of
    "makePrediction.prediction()" is used by webworldwind"""
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

"""The script runs automatically at 1 am EST. The timezone used depends on the timezone
of the pc or server running the scripts"""
schedule.every().day.at("01:00").do(call_daily)
while True:
    schedule.run_pending()
    time.sleep(1)
    

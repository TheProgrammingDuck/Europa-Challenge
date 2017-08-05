'''
Author: Vishal Soomaney

@License: MIT, See License.txt at root of project. 


This code generates the input CSV that the model makes its predictions based upon. 

'''
import requests
import time as times
import pandas as pd
import numpy as np

class Weather_data(object):

    def __init__(self, file, key, filesize):

        self.file=file
        self.key=key
        self.forest_locations=self.csv_to_array(self.file)

        #this tells you how many forests you're dealing with
        self.size= filesize
        
        
    def csv_to_array(self, file):    
        forest_locations=(np.genfromtxt(file, delimiter=','))
        forest_locations= forest_locations.tolist()

        #print(forest_locations)
        
        return(forest_locations)
    

    #nodays tells you number of days of data you want. Can be 1 or 2
    def get_Data(self,key, nodays ):     

        current_time= int(times.time())
        all_data=[]
        
        if nodays==1:
            input_times = [(current_time-86400)]
        elif nodays==2:
            input_times = [(current_time-86400),(current_time-172800)]
        else:
            print("nodays value can only be 1 or 2")
        
        for loc in self.forest_locations:
            
            locationCount=0

            for time in input_times:
                count=0
                locationCount+=1 

                response = requests.get("https://api.darksky.net/forecast/" + key + "/" + str(loc[0]) + "," + str(loc[1]) + "," + str(time) + "?units=si")
                
                data = response.json()
                #print(data)
                hourly_data = data['hourly']['data']
               
                
                location_array=[]
                temperature_array=[]
                humidity_array=[]
                wind_array=[]

                #Slightly hacky but counts amount of hours that contained rain. 0 hours= none (0),1-2 hours = little(1), 3-4 hours= medium(2), 5-7 hours= lot(3), 8+= massive amount(4)                rain_counter=0
                rain_counter=0
                rain_amount=0

                hour_counter=0

                #Checks weather data per hour, appends to an array then averages the data.
                
                for element in hourly_data:
                    #print(count)
                    count+=1
                    
                    #location_array.append(loc)
                    #hourly_array.append(int(element['time']))
                    temperature_array.append(element['temperature'])
                    humidity_array.append(element['humidity']*100)
                    wind_array.append(element['windSpeed'])
                    
                    if(element['precipIntensity'])==0:
                        pass 
                    else:
                        rain_counter+=1

                    hour_counter+=1

                    #if hour_counter==24:
                if rain_counter==0:
                    pass
                elif rain_counter<3:
                    rain_amount=1
                elif rain_counter<5:
                    rain_amount=2
                elif rain_counter<8:
                    rain_amount=3
                else:
                    rain_amount=4
                #print(sum(humidity_array)/float(len(humidity_array)))
                temp_list=[]
                temp_list.append(locationCount)
                temp_list.append(loc[0])
                temp_list.append(loc[1])
                temp_list.append(sum(temperature_array)/float(len(temperature_array)))
                temp_list.append(sum(humidity_array)/float(len(humidity_array)))
                temp_list.append(sum(wind_array)/float(len(wind_array)))
                temp_list.append(rain_amount)
                
                all_data.append(temp_list)
                location_array=[]
                temperature_array=[]
                humidity_array=[]
                wind_array=[]

                #Slightly hacky but counts amount of hours that contained rain. 0 hours= none (0),1-2 hours = little(1), 3-4 hours= medium(2), 5-7 hours= lot(3), 8+= massive amount(4)                rain_counter=0
                rain_counter=0
                rain_amount=0

                hour_counter=0
                        
                        
        #print(all_data)
        return( all_data)

    #imports the current csv and adds either 1 or 2 more days of data to each location
    def add_dayData(self, days):
        all_data= self.get_Data(self.key, days)
        currentData=(np.genfromtxt("initial.csv",delimiter=','))
        #print(currentData[0])
        currentData= currentData.tolist()
        dataCounter=0
        new_data=[]

        #Here we're calculating the number of days of data we have per location
        currentData.pop(0)
        currentDays= len(currentData)/self.size
        
        #print(currentDays)

        #for each location, if its the last day of data we have for that location, append the new data to the end of it.
        #the all_data array contains 2 days of data per location, so once you get past the last element per location, add 2 to the counter.
        for element in currentData:
            #print(element[0])
            
            # if we have 14 days of data per location, get rid of the first two whilst adding to the end.
            if currentDays==14:
                if days==2:
                    if element[0]==1 or element[0]==2:
                        pass
                    elif element[0]== currentDays:
                        new_data.append(element)
                        all_data[dataCounter][0]=currentDays+1
                        all_data[dataCounter+1][0]=currentDays+2
                        new_data.append(all_data[dataCounter])
                        new_data.append(all_data[dataCounter+1])
                        dataCounter+=days
                    else:
                        new_data.append(element)

                elif days==1:
                    if element[0]==1:
                        pass
                    
                    elif element[0]== currentDays:
                        new_data.append(element)
                        all_data[dataCounter][0]=currentDays+1
                        new_data.append(all_data[dataCounter])
                    else:
                        new_data.append(element)
                        
            else:
                if element[0]== currentDays:
                    new_data.append(element)
                    all_data[dataCounter][0]=currentDays+1
                    new_data.append(all_data[dataCounter])
                    if days==2:
                        all_data[dataCounter+1][0]=currentDays+2
                        new_data.append(all_data[dataCounter+1])
                    dataCounter+=days
                else:
                    new_data.append(element)

        return(new_data)
               

    def produce_Output(self, which):

        if (which)== "initial":
            all_data= self.get_Data(self.key, 2)
            name="initial.csv"
        elif (which)== "add1":
            all_data= self.add_dayData(1)
            name="initial.csv"
        elif(which)=="add2":
            all_data= self.add_dayData(2)
            name="initial.csv"
        elif(which)=="future":
            all_data= self.getFutureData(self.key)
            name="future.csv"
        else:
            print("Wrong produce_Output parameters entered")

        #print( all_data[2])

        df= pd.DataFrame(all_data,columns=["Days", "Longitude","Latitude", "Temp1", "Hum1","Wind1", "Rain"])

        df = df.set_index('Days')
        #print(df)
        df.to_csv(name)

    #Will produce a csv that gives past week averages
    def produce_final(self):
        currentData=(np.genfromtxt("initial.csv",delimiter=','))
        currentData= currentData.tolist()

        currentData.pop(0)
        currentDays= len(currentData)/self.size
        
        temperatureavg=0
        humavg=0
        windavg=0
        rainavg=0
        tempArray=[]
        
        avgArray=[]
        for element in currentData:
            humavg+=element[4]
            temperatureavg+=element[3]
            windavg+=element[5]
            rainavg+=element[6]
            
            if element[0]==currentDays:
                
                humavg=humavg/currentDays
                temperatureavg=temperatureavg/currentDays
                windavg=round(windavg/currentDays)
                rainavg=round(rainavg/currentDays)
                #print(rainavg)

                #tempArray.append(element[1])
                #tempArray.append(element[2])
                tempArray.append(temperatureavg)
                tempArray.append(humavg)
                tempArray.append(windavg)
                tempArray.append(rainavg)

                avgArray.append(tempArray)
                tempArray=[]
                temperatureavg=0
                humavg=0
                windavg=0
                rainavg=0
        
        df= pd.DataFrame(avgArray,columns=["Tempavg", "Humavg","Windavg", "Rainavg"])

        #print(df)
        df.to_csv("weather.csv")       

    def getFutureData(self, key):

        all_data=[]
        for loc in self.forest_locations:

            response = requests.get("https://api.darksky.net/forecast/" + key + "/" + str(loc[0]) + "," + str(loc[1]) + "?units=si")
            data = response.json()
            #print(data)
            daily_data = data['daily']['data']

            #Slightly hacky but counts amount of hours that contained rain. 0 hours= none (0),1-2 hours = little(1), 3-4 hours= medium(2), 5-7 hours= lot(3), 8+= massive amount(4)                rain_counter=0
            rain_amount=0

            day_counter=0
            count=0
            #Checks weather data per hour, appends to an array then averages the data.
            
            for element in daily_data:
                #print(count)
                count+=1
                
                if(element['precipIntensity'])<=0.35:
                    rain_amount=0
                elif (element['precipIntensity'])<=0.85:
                    rain_amount=1
                elif (element['precipIntensity'])<=1.4:
                    rain_amoount=2
                elif (element['precipIntensity'])<=1.9:
                    rain_amount=3
                else:
                    rain_amount=4

                if day_counter<6:
                
                    temp_list=[]
                    temp_list.append(day_counter)
                    temp_list.append(loc[0])
                    temp_list.append(loc[1])
                    temp_list.append(((element['apparentTemperatureMin'])+element['apparentTemperatureMax'])/2)
                    temp_list.append(element['humidity']*100)
                    temp_list.append(element['windSpeed'])
                    temp_list.append(rain_amount)
                    
                    all_data.append(temp_list)
                    day_counter+=1

                else:
                    pass

        return(all_data)
                   

    def output_to_svm(self):
        currentData=(np.genfromtxt("weather.csv",delimiter=','))
        currentData= currentData.tolist()
        currentData.pop(0)

        futureData=(np.genfromtxt("future.csv",delimiter=','))
        futureData= futureData.tolist()
        futureData.pop(0)

        finalArray=[]
        counter=0
        location=0
        for element in futureData:
            #print(currentData[location])
            #print(element)
            element.extend(currentData[location][1:5])
            #print(element)
            finalArray.append(element)
            counter+=1
            if counter==6:
                location+=1
                counter=0

        #print(finalArray)
        df= pd.DataFrame(finalArray,columns=["Days", "Longitude","Latitude", "AvgTemp", "AvgHum","AvgWind", "AvgRain", "14dayAvgTemp", "14dayAvgHum", "14dayAvgWind", "14dayAvgRain"])
        df.to_csv("finalweather.csv")

                
file='forest_locations.csv'
key = 'e5d530b79eb4c2232e41a7ab30a208e4'

#weatherGetter = Weather_data(file,key, 193)
#weatherGetter.produce_Output("initial")
#weatherGetter.produce_final()
#weatherGetter.produce_Output("future")
#weatherGetter.output_to_svm()




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
                    
                    count+=1

                    #Add hourly data to temporary arrays
                    temperature_array.append(element['temperature'])
                    humidity_array.append(element['humidity']*100)
                    wind_array.append(element['windSpeed'])
                    
                    if(element['precipIntensity'])==0:
                        pass 
                    else:
                        rain_counter+=1

                    hour_counter+=1

                #checking number of hours that contain rain. Ideally we use use mm/hour however we need to use the same standards used in the training data.  
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

                #Once you have hourly weather data, you merge it to obtain daily averages
                temp_list=[]
                temp_list.append(locationCount)
                temp_list.append(loc[0])
                temp_list.append(loc[1])
                temp_list.append(sum(temperature_array)/float(len(temperature_array)))
                temp_list.append(sum(humidity_array)/float(len(humidity_array)))
                temp_list.append(sum(wind_array)/float(len(wind_array)))
                temp_list.append(rain_amount)

                #you append the daily averages to a final array
                all_data.append(temp_list)

                #emptying arrays for next location
                location_array=[]
                temperature_array=[]
                humidity_array=[]
                wind_array=[]

                #zeroing variables for next location
                rain_counter=0
                rain_amount=0

                hour_counter=0
                        
        return(all_data)

    #imports the current csv and adds either 1 or 2 more days of data to each location
    #The "days" parameter determines how many days of data you are adding to each location
    def add_dayData(self, days):
        all_data= self.get_Data(self.key, days)
        currentData=(np.genfromtxt("initial.csv",delimiter=','))
        currentData= currentData.tolist()
        #keeps track of what position you're on in the array obtained from the get_Data method
        dataCounter=0
        new_data=[]

        #Here we're calculating the number of days of data we have per location
        currentData.pop(0)
        currentDays= len(currentData)/self.size
        

        #for each location, if its the last day of data we have for that location, append the new data to the end of it.
        #the all_data array contains 2 days of data per location, so once you get past the last element per location, add 2 to the counter.
        for element in currentData:
            #print(element[0])
            
            #if we have 14 days of data per location, get rid of the first two whilst adding to the end.
            if currentDays==14:
                if days==2:
                    #element[0] contains the index, it tells you which day of data you are on. Does that row show the 5th day of data for that location or the 14th.
                    #If there's already 14 days of data, simply don't append the 2 oldest days of data to the new array.
                    if element[0]==1 or element[0]==2:
                        pass
                    elif element[0]== currentDays:
                        #As we've removed the 2 oldest days of data, we must update the indexes of the rest
                        element[0]=element[0]-1
                        
                        new_data.append(element)
                        #Updating the indexes of the 2 next days of data in the array obtained from the get_Data method
                        all_data[dataCounter][0]=currentDays-1
                        all_data[dataCounter+1][0]=currentDays
                        #Appending this to the new array
                        new_data.append(all_data[dataCounter])
                        new_data.append(all_data[dataCounter+1])
                        dataCounter+=days
                    else:
                        element[0]=element[0]-1
                        new_data.append(element)

                elif days==1:
                    if element[0]==1:
                        pass
                    
                    elif element[0]== currentDays:
                        #As we're removing he oldest day of data, we must update the indexes of the rest
                        element[0]=element[0]-1
                        #Appended data from day 14, changing index to show its day 13
                        new_data.append(element)
                        #Data from the day whose data was just retrieved by the api
                        all_data[dataCounter][0]=currentDays
                        new_data.append(all_data[dataCounter])
                        dataCounter+=1
                    else:
                        #If there's 14 days of data per location but you aren't currently iterating over the 14th day then just adjust the index and append it to the new array
                        element[0]= element[0]-1
                        print(element[0])
                        new_data.append(element)

                    #If there's not already 14 days of data per location then just append all the data from the imported csv to the new array   
            else:
                if element[0]== currentDays:
                    new_data.append(element)
                    #add the new day of data obtained from the get_Data method to the bottom of each location with the correct index.
                    #ie: if there's currently 5 days of data per location, add the new day with an index of 6.
                    all_data[dataCounter][0]=currentDays+1
                    new_data.append(all_data[dataCounter])
                    if days==2:
                        all_data[dataCounter+1][0]=currentDays+2
                        new_data.append(all_data[dataCounter+1])
                    dataCounter+=days
                else:
                    new_data.append(element)

        return(new_data)
               
    #A method to simplify usage of the class. Can be used to call a method that returns an array and turn that array into a csv.
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

        df= pd.DataFrame(all_data,columns=["Days", "Longitude","Latitude", "Temp1", "Hum1","Wind1", "Rain"])
    
        df = df.set_index('Days')
        #Many are called a similar name as they simply add a day onto the main csv and overwrite it
        df.to_csv(name)

    #Will produce a csv that gives 14 day averages
    def produce_average(self):
        currentData=(np.genfromtxt("initial.csv",delimiter=','))
        currentData= currentData.tolist()

        #removes column headings
        currentData.pop(0)
        currentDays= len(currentData)/self.size
        
        temperatureavg=0
        humavg=0
        windavg=0
        rainavg=0
        tempArray=[]

        #counts how many empty days of data there are for each location
        zeroedvalues=0
        
        avgArray=[]
        for element in currentData:
            #if both temperature and humidity are 0 then it's a zeroed day
            if element[4]==0 and element[5]==0:
                zeroedvalues+=1
            else:
                #add data to temporary arrays until you reach the end of the data you have for that location
                humavg+=element[4]
                temperatureavg+=element[3]
                windavg+=element[5]
                rainavg+=element[6]
            
            if element[0]==currentDays:
                if zeroedvalues==currentDays:
                    zeroedvalues-=1
                    
                #temporary arrays are used to calculate averages    
                humavg=humavg/(currentDays-zeroedvalues)
                temperatureavg=temperatureavg/(currentDays-zeroedvalues)
                windavg=round(windavg/(currentDays-zeroedvalues))
                rainavg=round(rainavg/(currentDays-zeroedvalues))

                #all averages are put into one array
                tempArray.append(temperatureavg)
                tempArray.append(humavg)
                tempArray.append(windavg)
                tempArray.append(rainavg)

                #this one array is nested into a final avgArray - nested arrays are required for conversion to csv.
                #Each nested array is a row
                avgArray.append(tempArray)
                
                tempArray=[]
                temperatureavg=0
                humavg=0
                windavg=0
                rainavg=0
                zeroedvalues=0
        
        df= pd.DataFrame(avgArray,columns=["Tempavg", "Humavg","Windavg", "Rainavg"])

        df.to_csv("averageWeather.csv")       

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
                   
#merges future weather data with past 14 day averages
    def output_to_svm(self):
        currentData=(np.genfromtxt("averageweather.csv",delimiter=','))
        currentData= currentData.tolist()
        currentData.pop(0)

        futureData=(np.genfromtxt("future.csv",delimiter=','))
        futureData= futureData.tolist()
        futureData.pop(0)

        finalArray=[]
        counter=0
        location=0
        for element in futureData:
            #appending averages to the end of the future weather data array
            element.extend(currentData[location][1:5])
            
            finalArray.append(element)
            counter+=1
            #We have forecasts for the next 6 days of data per location
            if counter==6:
                location+=1
                counter=0

        df= pd.DataFrame(finalArray,columns=["Days", "Longitude","Latitude", "AvgTemp", "AvgHum","AvgWind", "AvgRain", "14dayAvgTemp", "14dayAvgHum", "14dayAvgWind", "14dayAvgRain"])
        df.to_csv("svmoutput.csv")

                
file='forest_locations.csv'
key = ''

weatherGetter = Weather_data(file,key, 210)
weatherGetter.produce_Output("initial")
weatherGetter.produce_average()
weatherGetter.produce_Output("future")
weatherGetter.output_to_svm()




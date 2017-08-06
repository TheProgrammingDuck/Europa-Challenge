'''
Author: Vishal Soomaney
@License: MIT, See License.txt at root of project. 

A script used to gather data on the internet.
'''
import csv
from bs4 import BeautifulSoup
import urllib.request
import json
import pandas as pd
import time

wildfires = []
fire_data = []
Counter=0
forests = {'0501':'La Cañada Flintridge', '0502':'Ramona',  ## maps forest_id to nearest city to forest
           '0503':'placerville', '0504':'Bishop',
           '0505':'yreka', '0506':'Susanville',
           '0507':'santa-barbara', '0508':'Willows',
           '0509':'Alturas', '0510':'Crescent City',
           '0511':'Quincy', '0512':'san-bernardino',
           '0513':'bakersfield', '0514':'redding',
           '0515':'Oakhurst', '0516':'Sonora',
           '0517':'truckee', '0519':'Tahoe City'}

locationUrl= {'La Cañada Flintridge':"@5363859",'Ramona':'@5385801','placerville':'placerville',
              'Bishop':"@5328808",'yreka':"yreka",'Susanville':'@5572400','santa-barbara':'santa-barbara','Willows':'@5402129',
              'Alturas':"@5558829",'Crescent City':"@5562087",'Quincy':"@5385487",'san-bernardino':'san-bernardino',
              'bakersfield':'bakersfield', 'redding':'redding',
           'Oakhurst':"@5378529", 'Sonora':"@5397151",
           'truckee':'truckee', 'Tahoe City':"@5400950"}

cityList=["@5363859",'@5385801','placerville',"@5328808",'yreka','@5572400','santa-barbara','@5402129',
          "@5558829","@5562087","@5385487",'san-bernardino','bakersfield','redding',"@5378529","@5397151","truckee","@5400950"]

fireDict={"@5363859":[],'@5385801':[],'placerville':[],"@5328808":[],'yreka':[],'@5572400':[],'santa-barbara':[],'@5402129':[],
          "@5558829":[],"@5562087":[],"@5385487":[],'san-bernardino':[],'bakersfield':[],'redding':[],"@5378529":[],"@5397151":[],"truckee":[],"@5400950":[] }
i = 0
x = []
y = []

data = []

#Setting up the csv containing 6.5 years of rain data.
with open('6_years.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if len(row)==0:
            #ignoring empty rows 
            pass
        else:
            wildfires.append(row)

for element in wildfires:
    element=[''.join(element)]
    for item in element:
        x = item.split('\t')
        #removing wildfires that took place due to arson, nearby children or railroads
        if (x[4]==7) or (x[4]==5) or (x[4]==6):
            pass
        else:
            data.append(x)


data = data[1:]

for element in data:

    #obtaining date and location for each wildfire
    day=str((str(element[17]).split()[0]))
    day=day.split("-")
    
    day= str(day[1]+"/"+day[2] + "/"+ day[0])

    """An array exists for each location we are obtaining data for. If a fire occurred in any of those
    locations, the date of that fire is added to the array"""
    fireDict[locationUrl[forests[element[0]]]].append(day)

carrot=[]
names=[]
dates=[]
   

finalArray=[]
dateCounter=0

#You can adjust contents of these 2 arrays to determine which months and years you want to scrape data for.
years=[2011,2012,2013,2014,2015,2016,2017]

months=[1,2,3,4,5,6,7,8,9,10,11,12]

#get the rain data for the entire month for each wildfire
for locationList in cityList:
    #Arrays that contain 14 day average rain data for each day for each location.
    lastWeekTemp=[]
    lastWeekHum=[]
    lastWeekWind=[]
    lastWeekRain=[]
    
    for year in years:
        for month in months:
            dateCounter+=1            

            #Keywords to filter data.
            r='temp'
            h='hum'
            w='wind'
            d='desc'
            ds='ds'

            #We append all the data points provided for a day in the temporary arrays.
            #Each of the temporary arrays are then appended to the main arrays.
            temperature=[]
            tempotemp=[]
            
            humidity=[]
            tempohum=[]
            
            wind=[]
            tempowind=[]
            
            currentDate=[]
            
            rain=[]

            
            fireList=[]

            #Contain daily averages, these are used to calculate 14 day averages.
            tempAvg=[]
            humAvg=[]
            windAvg=[]
            rainAvg=[]            

            #counters 
            humcount=0
            windcount=0
            tempcount=0
            weathcount=0
            tempoweath=0
            dscount=0

            dateNum=0

            #counting how many empty data points there are for a day, necessary when calculating averages.
            tempnonz=0
            windnonz=0
            humnonz=0

            number=0
            tempBool=False
            humBool=False
            windBool=False
            dbool=False
            dsbool=False

            #There exist 2 different types of URL on the website depending on the location. This method allows beautifulsoup to adapt to it.
            def scrapeData():
                if locationList[0]=="@":
                    with urllib.request.urlopen(""%(locationList, month, year))  as url:
                        s = url.read()
                else:
                    with urllib.request.urlopen(""%(locationList, month, year))  as url:
                        s = url.read()
                
                soup = BeautifulSoup(s, "html5lib")
                soup.prettify()
                scrapedText= str(soup.find_all("script")[5])
                
                scrapedText=str(scrapedText.replace("}",""))
                scrapedText=str(scrapedText.split('"ds"',1)[1])
                return (scrapedText)

            #From time to time there's an issue with the website we are scraping from, we assume that it's being updated with new data, trying again fixes the issue.
            def errorCatcher():
                while True:
                    try:
                        print("Attempting New Month")
                        return(scrapeData()) 
                    except Exception:
                        print("Error")
                        time.sleep(5)
            scrapedText=errorCatcher()

            #turn into string and iterate through all "temp" and add the integers next to it to an array then get avg.
            scrapedText=str(scrapedText.split(','))
            scrapedText=str(scrapedText.split(':'))
            scrapedText=scrapedText.replace("'","")
            scrapedText=scrapedText.replace('\\',"")
            scrapedText=scrapedText.replace('"',"")
            scrapedText=scrapedText.replace("}","")
            scrapedText=scrapedText.replace(",","")
            scrapedText=scrapedText.replace(']',"")
            scrapedText=scrapedText.split()
            
            
            for word in scrapedText:
                
                if word=='{offset':
                    tempBool=False
                    humBool=False
                    windBool=False


                """If the current element is a temperature, tempBool becomes true.
                This checks for that"""
                if tempBool== True:
                    #converting the temperature from string to float
                    word=float(word)
                    """Appending the temperature to a temporary temperature array
                    The temperature array contains at most 4 temperatures at any given time."""
                    tempotemp.append(word)
                    tempcount+=1

                    
                    """If the value of temperature is not 0, then add 1 to a variable.
                    This keeps track of how many data points we don't have values for.
                    It comes in handy for calculating averages"""
                    if word!=0.0:
                        tempnonz+=1
                    
                    tempBool=False
                """There's 4 temperature data points every day, this keeps track of how many have
                been added to the temporary array. Once there's 4, both them and the daily averages
                calculated from them are added to the final temperature array"""
                if tempcount==4:
                   
                    if (sum(tempotemp)/float(len(tempotemp)))== 0:
                        tempotemp.append("no data") 
                    else:
                        #Here we calculate the average and append it to the end of the temporary array
                        tempotemp.append(sum(tempotemp) / float(tempnonz))

                        """Keeps track of the last 14 days of rain data, used to provide the past
                        14 day rain average for every day"""
                        if len(lastWeekTemp)==14:
                            lastWeekTemp.pop(0)

                        #We append daily average to it (last element in the temporary array is the average)
                            lastWeekTemp.append(tempotemp[4])
                        else:
                            
                            lastWeekTemp.append(tempotemp[4])
                    tempAvg.append(sum(lastWeekTemp) / float(len(lastWeekTemp)) )
                    #We append the 4 data points + average array to a final temperature array
                    temperature.append(tempotemp)
                    #We zero everything readying it for when the next temperature value is found
                    tempnonz=0
                    tempcount=0
                    tempotemp=[]
                    
                #The methodology for this is exactly the same as the method for temperature    
                if humBool==True:
                    word=float(word)
                    tempohum.append(word)
                    humcount+=1
                    if word!=0.0:
                        humnonz+=1
                    if humcount==4:
                        if (float(sum(tempohum))/float(len(tempohum)))== 0:
                            tempohum.append("No Data") 
                        else:
                            tempohum.append(sum(tempohum) / float(humnonz))
                            if len(lastWeekHum)==14:
                                lastWeekHum.pop(0)
                                lastWeekHum.append(tempohum[4])
                            else:
                                lastWeekHum.append(tempohum[4])
                        humAvg.append(sum(lastWeekHum) / float(len(lastWeekHum)) )
                        humidity.append(tempohum)
                        tempohum=[]
                        humcount=0
                        humnonz=0
                    humBool=False
                    
                #Same method as for temperature and humidity
                if windBool==True:
                    word=float(word)
                    tempowind.append(word)
                    windcount+=1
                    if word!=0.0:
                        windnonz+=1
                    if windcount==4:
                        if (sum(tempowind)/float(len(tempowind)))== 0:
                            tempowind.append("No Data")
                        else:
                            tempowind.append(sum(tempowind) / float(windnonz))
                            if len(lastWeekWind)==14:
                                lastWeekWind.pop(0)
                                lastWeekWind.append(tempowind[4])
                            else:
                                lastWeekWind.append(tempowind[4])
                        windAvg.append(int(round(sum(lastWeekWind) / float(len(lastWeekWind)))))
                            
                        wind.append(tempowind)
                        tempowind=[]
                        windcount=0
                        windnonz=0
                    windBool=False

                #Checking if there was rain on a given day and if there was, how much was there.
                if dbool==True:
                    weathcount+=1
                    if word=="No rain data available":
                        tempotemp.append(0)
                        tempocount+=1
                    if word=="Thundershowers.":
                        tempoweath+=1
                        #Providing rain data as a number from 0-4.
                    if weathcount==4:
                        if tempoweath==0:
                            rain.append("0")
                        if tempoweath==1:
                            rain.append("1")
                        if tempoweath==2:
                            rain.append("2")
                        if tempoweath==3:
                            rain.append("3")
                        if tempoweath==4:
                            rain.append("4")
                        #Providing 14 day rain averages
                        if len(lastWeekRain)==14:
                            lastWeekRain.pop(0)
                            lastWeekRain.append(tempoweath)
                        else:
                            lastWeekRain.append(tempoweath)
                        rainAvg.append((sum(lastWeekRain)/len(lastWeekRain)) )
                        #Zeroing everything for next round
                        tempoweath=0
                        weathcount=0
                    dbool=False

                #Checking the full date for the data being scraped and appending it to an array so it can be shown on the final csv.
                if dsbool==True:
                    if dscount==1:
                        if word=="1":
                            word="01"
                        if word=="2":
                            word="02"
                        if word=="3":
                            word="03"
                        if word=="4":
                            word="04"
                        if word=="5":
                            word="05"
                        if word=="6":
                            word="06"
                        if word=="7":
                            word="07"
                        if word=="8":
                            word="08"
                        if word=="9":
                            word="09"
                        tempword=word
                        dscount+=1
                    elif dscount==2:
                        if word=="January":
                            word="01"
                        if word=="February":
                            word="02"
                        if word=="March":
                            word="03"
                        if word=="April":
                            word="04"
                        if word=="May":
                            word="05"
                        if word=="June":
                            word="06"
                        if word=="July":
                            word="07"
                        if word=="August":
                            word="08"
                        if word=="September":
                            word="09"
                        if word=="October":
                            word="10"
                        if word=="November":
                            word="11"
                        if word=="December":
                            word="12"
                        tempword2=word
                        dscount+=1
                    elif dscount==3:
                        tempyear=word
                        currentDate.append(str(tempword2)+"/"+str(tempword)+"/"+str(tempyear))
                        dscount=0
                        dsbool=False
                    else:
                        dscount+=1
                    
                #Going through each word in the scraped and filtered code to if a useful keyword is found, ie "temp". When it's found, the relevant boolean becomes true.    
                if word==r:
                    tempBool=True
                if word==h:
                    humBool=True
                if word==w:
                    windBool=True
                if word==d:
                    dbool=True
                if word==ds:
                    if dateNum==0:
                        dateNum+=1
                        dsbool=True
                    elif dateNum==1:
                        dateNum+=1
                    elif dateNum==2:
                        dateNum+=1
                    elif dateNum==3:
                        dateNum=0
                        

            #For each date we have rain data for
            for each in currentDate:
                currentBool=0
                #If there was a fire on that day, append 1 to fireList, else append 0.
                for day in fireDict[locationList]:
                    
                    if each==day:
                        currentBool=1
                    else:
                        pass
                fireList.append(currentBool)

            """Merge arrays for all data types to create 1 massive array of arrays. Each array within it represents 1 day of data.
            This works since there's exactly the same amount of data for each data type.
            We also append a boolean indicating whether there was a fire or not on that day to the arrays."""
            for each in range(len(temperature)): 
                finalArray.append(temperature[each]+humidity[each]+wind[each])
                finalArray[Counter].append(currentDate[each])
                finalArray[Counter].append(rain[each])
                finalArray[Counter].append(rainAvg[each])
                finalArray[Counter].append(tempAvg[each])
                finalArray[Counter].append(humAvg[each])
                finalArray[Counter].append(windAvg[each])
                """We append the name of the location we are appending data for to the array""" 
                finalArray[Counter].append((list(locationUrl.keys())[list(locationUrl.values()).index(locationList)]))
                finalArray[Counter].append(fireList[each])
                Counter+=1



df= pd.DataFrame(finalArray,columns=["Temp1","Temp2", "Temp3","Temp4", "avgTemp", "Hum1","Hum2","Hum3","Hum4"
                                     ,"avgHum","Wind1","Wind2","Wind3","Wind4","avgWind", "CurrentDate", "Rain"
                                     ,"14DayAvgRain","14DayAvgTemp", "14dayAvgHum", "14DayAvgWind", "Location" ,"Fire"])

df = df.set_index('CurrentDate')

df.to_csv("MergedWildfireweather.csv")
                            



'''
Author: Flinn Dolman

@License: MIT, See License.txt at root of project. 

Method calls to this object serve the purpose of preparing data for the model and saving/loading the scale used to train the model.
The same scale must be used to standardise data used for predicitions which is why this is important. There also exists a method
for performing PCA analysis on data.

'''

import pandas as pd
import numpy as np
import random
from sklearn.model_selection import train_test_split #splitting up data for testing
from sklearn import preprocessing #standardisation of data
from sklearn.externals import joblib #saving/loading the scale used for standardising the data during training

from sklearn.decomposition import PCA #principal component analysis
import random

class Standardiser:
	def __init__(self):
		pass

	#load in data, then standardise and split it for training/testing.
	def initialise(self):

		print("standardiser initialising")
		self.data = self.loadData()
		self.X_train, self.X_test, self.y_train, self.y_test = self.splitData(self.data)
		self.std_scale, self.X_train_std, self.X_test_std = self.standardise(self.X_train, self.X_test, self.y_train, self.y_test)

	#getter functions for retreiving split standardised data	
	def get_std_X_train(self):
		return self.X_train_std
	
	def get_std_X_test(self):
		return self.X_test_std
	
	def get_y_train(self):
		return self.y_train	

		
	def get_y_test(self):
		return self.y_test
		
	#read in the data as a pandas dataframe. ignore the first row (headers) and only use columns PCA deemed good for training on.
	def loadData(self):
		
		df = pd.io.parsers.read_csv(
                        'Data/NewBalanced.csv',
                        header=None,
                        skiprows = [0],
                        usecols=[5,10,15,17,18,19,20,22])		
		return df	

	#loads in Darkskies weather predictions for the coming week.
	def loadForecast(self,forecast_loc):

		#load in forecast csv
                self.foredf = pd.io.parsers.read_csv(
                        forecast_loc,
                        header=None,
                        skiprows = [0],
                        usecols=[1,2,3,4,5,6,7,8,9])
                X_forecast = self.foredf.values[:,3:]
                X_forecast = self.standardise_Pred(X_forecast)
                return X_forecast	

			
    #split data into training and testing samples
	def splitData(self, data):
		X = data.values[:,:7]
	
		y = data.values[:,7]
	
		#split the data into training and testing data
		X_train, X_test, y_train, y_test = train_test_split(X, y,
			test_size=0.30, random_state=random.randint(10,100000))
		
		return X_train, X_test, y_train, y_test

			
			
			
	#standardise the data and save the scale it was standardised on.		
	def standardise(self, X_train, X_test, y_train, y_test):
		#standardisation using sklearn
                self.std_scale = preprocessing.StandardScaler().fit(X_train)
                X_train_std = self.std_scale.transform(X_train)
                X_test_std = self.std_scale.transform(X_test)
                self.saveScale()
                return self.std_scale, X_train_std, X_test_std


	#standardises data readin for prediction
	def standardise_Pred(self, X_forecast):
		X_forecast_std = self.std_scale.transform(X_forecast)
		return X_forecast_std

	#performs PCA on the traning data.
	def PCAan(self, X_train_std, X_test_std, y_train):

		pca_std = PCA(n_components=2).fit(X_train_std)
		X_train_std = pca_std.transform(X_train_std)
		X_test_std = pca_std.transform(X_test_std)

		return pca_std, X_train_std, X_test_std

	#appends forecast predictions (both class and probability based) to the svm input csv and then produces a new svmoutput csv 
	def make_CSV(self, fore_pred, fore_prob,outputfile):
		print("make_CSV")
		forearray = self.foredf.values.tolist()
		i = 0
		for element in forearray:
                        element.append(fore_pred[i])
                        element.append(fore_prob[i][1])
                        i +=1

		df = pd.DataFrame(forearray)
		df.to_csv(outputfile)

	#save the scale standardised on
	def saveScale(self):
                print("saveScale")
                joblib.dump(self.std_scale, 'Models/Scaler.pkl')
    #load the scale standardised on          
	def loadScale(self):
                print("loadScale")
                self.std_scale = joblib.load('Scaler.pkl')

import pandas as pd
import numpy as np
import random
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.externals import joblib

from sklearn.decomposition import PCA
import random

class Standardiser:
	def __init__(self):
		pass

	def initialise(self):
		#self.input = input
		print("standardiser initialising")
		self.data = self.loadData()
		self.X_train, self.X_test, self.y_train, self.y_test = self.splitData(self.data)
		self.std_scale, self.X_train_std, self.X_test_std = self.standardise(self.X_train, self.X_test, self.y_train, self.y_test)
		#self.std_scale, self.X_train_std, self.X_test_std = self.PCAan(self.X_train, self.X_test, self.y_train)
		
		#standardised
		#pca_std, X_train_stdpca, X_test_stdpca = PCAan(X_train_std, X_test_std)
		
		#non standardised
		#pca_std, X_train_stdpca, X_test_stdpca = PCAan(X_train, X_test)
		
		#genGraph(pca_std, X_train_stdpca, X_test_stdpca, y_train)
		
	def get_std_X_train(self):
		return self.X_train_std
	
	def get_std_X_test(self):
		return self.X_test_std
	
	def get_y_train(self):
		return self.y_train	

		
	def get_y_test(self):
		return self.y_test
		
	def loadData(self):
		
		df = pd.io.parsers.read_csv(
                        'Data/NewBalanced.csv',
                        header=None,
                        skiprows = [0],
                        usecols=[5,10,15,17,18,19,20,22])		
		return df	

	def loadForecast(self,forecast_loc):

		#load in forecast csv
                self.foredf = pd.io.parsers.read_csv(
                        forecast_loc,
                        header=None,
                        skiprows = [0],
                        usecols=[1,2,3,4,5,6,8,9,10])
                X_forecast = self.foredf.values[:,3:]
                X_forecast = self.standardise_Pred(X_forecast)
                return X_forecast	

			


	def splitData(self, data):
		X = data.values[:,:7]
	
		y = data.values[:,7]
	
		#split the data into training and testing data
		X_train, X_test, y_train, y_test = train_test_split(X, y,
			test_size=0.30, random_state=random.randint(10,100000))
		
		return X_train, X_test, y_train, y_test

			
			
			
			
	def standardise(self, X_train, X_test, y_train, y_test):
		#standardisation using sklearn
                self.std_scale = preprocessing.StandardScaler().fit(X_train)
                X_train_std = self.std_scale.transform(X_train)
                X_test_std = self.std_scale.transform(X_test)
                self.saveScale()
                return self.std_scale, X_train_std, X_test_std


	def standardise_Pred(self, X_forecast):
		X_forecast_std = self.std_scale.transform(X_forecast)
		return X_forecast_std

	def PCAan(self, X_train_std, X_test_std, y_train):

		pca_std = PCA(n_components=2).fit(X_train_std)
		X_train_std = pca_std.transform(X_train_std)
		X_test_std = pca_std.transform(X_test_std)
		#genGraph(pca_std, X_train_std, X_test_std, y_train)
		return pca_std, X_train_std, X_test_std


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

	def saveScale(self):
                print("saveScale")
                joblib.dump(self.std_scale, 'Models/Scaler.pkl')
                
	def loadScale(self):
                print("loadScale")
                self.std_scale = joblib.load('Scaler.pkl')

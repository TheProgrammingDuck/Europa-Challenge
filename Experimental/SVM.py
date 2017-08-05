'''
Author: Flinn Dolman

@License: MIT, See License.txt at root of project. 

This object trains the model as well as interfacing for prediction using the model.
It can also show the accuracy of the trained model and saves and loads models to be used.

'''
from sklearn.svm import SVC #Scikit learn library for support vector machine training 
from sklearn.externals import joblib
import numpy as np

class SVM:
	
	
	def __init__(self):
		
		pass

	#gives the SVM object the training and testing data. it then invokes the classification method for training the model 		
	def initialise(self, X_train, X_test, y_train, y_test):

                self.X_train = X_train
                self.X_test = X_test
                self.y_train = y_train
                self.y_test = y_test
                self.classify()

    #actual training of the model occurs here. a classifier is instantiated from sklearn and then it is fitted to our data.
	def classify(self):

		self.clf = SVC(C=1.0, cache_size=200, class_weight='balanced', coef0=0.0,
			decision_function_shape=None, degree=3, gamma='auto', kernel='rbf',
			max_iter=-1, probability=True, random_state=None, shrinking=True,
			tol=0.001, verbose=False) 
		
		self.clf.fit(self.X_train,self.y_train)
		
	#makes class and probability based predictions based upon the values in the test datasets.	
	def predictions(self):
		
		return self.clf.predict(self.X_test), self.clf.predict_proba(self.X_test)

	#makes predictions for the darksky gathered data
	def forecast_Pred(self,X_forecast):
		
		return self.clf.predict(X_forecast), self.clf.predict_proba(X_forecast)	
		
	#returns the accuracy that the model has obtained after training	
	def accuracy(self):
	
		return self.clf.score(self.X_test, self.y_test, sample_weight=None)
		
	#saves the model so that it can be reused
	def saveModel(self):
                print("svm saving model")
                joblib.dump(self.clf, 'Models/Model.pkl')
    
    #loads in the model for use            
	def loadModel(self):
                print("svm loading model")
                self.clf = joblib.load('Model.pkl')

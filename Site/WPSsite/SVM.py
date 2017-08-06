from sklearn.svm import SVC
from sklearn.externals import joblib
import numpy as np

class SVM:
	
	
	def __init__(self):
		
		pass
		#self.X_train = X_train
		#self.X_test = X_test
		#self.y_train = y_train
		#self.y_test = y_test
		#self.classify()
		
	def initialise(self, X_train, X_test, y_train, y_test):
                print("SVM initialising")
                self.X_train = X_train
                self.X_test = X_test
                self.y_train = y_train
                self.y_test = y_test
                self.classify()

	def classify(self):
		print("svm classifying")
		self.clf = SVC(C=1.0, cache_size=200, class_weight='balanced', coef0=0.0,
			decision_function_shape=None, degree=3, gamma='auto', kernel='rbf',
			max_iter=-1, probability=True, random_state=None, shrinking=True,
			tol=0.001, verbose=False) 
		
		self.clf.fit(self.X_train,self.y_train)
		
		
	def predictions(self):
		
		return self.clf.predict(self.X_test), self.clf.predict_proba(self.X_test)


	def forecast_Pred(self,X_forecast):
		
		return self.clf.predict(X_forecast), self.clf.predict_proba(X_forecast)	
		
		
	def accuracy(self):
	
		return self.clf.score(self.X_test, self.y_test, sample_weight=None)
		
	
	def saveModel(self):
                print("svm saving model")
                joblib.dump(self.clf, 'Models/Model.pkl')
                
	def loadModel(self):
                print("svm loading model")
                self.clf = joblib.load('Model.pkl')

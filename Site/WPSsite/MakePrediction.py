from SVM import SVM
from Standardiser import Standardiser

class MakePrediction(object):

        def __init__(self):
                self.standard_data = Standardiser()
                print("standardiser started")
                self.standard_data.loadScale()
                print("scale loaded")
                self.clf = SVM()
                print("svm loaded")
                self.clf.loadModel()
                print("model loaded")
                self.outputfile = 'svmoutput.csv'
                self.forecast_loc = 'finalweather.csv'
        

        def prediction(self):
                print("Make Prediction started")
                fore_Pred, fore_Prob = self.clf.forecast_Pred(self.standard_data.loadForecast(self.forecast_loc))
                print("predictions made")
                self.standard_data.make_CSV(fore_Pred,fore_Prob, self.outputfile)
                print("output csv made")	

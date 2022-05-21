import pandas as pd
from sklearn import linear_model 
from sklearn.model_selection import train_test_split
from datetime import datetime
from catboost import CatBoostRegressor 
from sklearn import preprocessing

carsDf = pd.read_json('./out3.json')
le = preprocessing.LabelEncoder()

carsDf = carsDf.drop('url', 1)
dataToPredict = pd.DataFrame.from_records([ 
   { "manufacturingYear": 2018, "kmOnBoard": 7000, "combustion": "Diesel", "brand": "Dacia"},
])

brand_dummies = pd.get_dummies(carsDf['brand'])
carsDf = pd.concat([carsDf, brand_dummies], axis=1)
carsDf = carsDf.drop('brand', 1)

carsDf['manufacturingYear'] = pd.to_numeric(carsDf['manufacturingYear'])
carsDf['age'] = datetime.now().year - carsDf['manufacturingYear']
carsDf = carsDf.drop('manufacturingYear', 1)

carsDf['combustion'] = le.fit_transform(carsDf['combustion']) 

X = carsDf.drop('price', 1)
Y = carsDf.price
X_train, X_test, y_train, y_test = train_test_split(
	X, Y, train_size = 0.7, test_size = 0.3, random_state = 100)

model = CatBoostRegressor(iterations = 6542, learning_rate = 0.03)
model.fit(
	X_train, y_train,
	eval_set=(X_test, y_test),
)

dataToPredict['combustion'] = le.fit_transform(dataToPredict['combustion']) 
dataToPredict['age'] = datetime.now().year - dataToPredict['manufacturingYear']
dataToPredict = dataToPredict.drop('manufacturingYear', 1) 

dataToPredictBrandDummy =  pd.get_dummies(dataToPredict['brand']);
dataToPredict = pd.concat([dataToPredict, dataToPredictBrandDummy], axis=1)
dataToPredict = dataToPredict.drop('brand', 1)
 
fitModel = pd.DataFrame(columns = carsDf.columns)
fitModel = fitModel.append(dataToPredict, ignore_index=True)

predictions = model.predict(fitModel) 
print('==========================')
print('Estimated price: ', int(predictions[0]))
print('Score: ', model.score(X,Y))
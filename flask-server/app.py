from flask import Flask
import pymongo
import purdue_covid19
app = Flask(__name__)

#update the data
purdue_covid19
#init the client
uri = "mongodb://database41:udZWotnoErEf7YK6FBsmAWrcbU85xaYHxRBJSGlImVaSYX3BOA2KdLmfXCHclqDoaWw6aiWV1AAAOd1RvqGJaw==@database41.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@database41@"
my_client = pymongo.MongoClient(uri)
#create the database
database = my_client["AIAzure_database"]
#Create collection
covid_data = database['Covid']
prediction_data = database['Prediction']

covid_query = {}
prediction_query = {}
for query in covid_data.find():
    covid_query = query
for query in prediction_data.find():
    prediction_query = query 
del covid_query['_id']       
@app.route('/')
def home():
  return {
      'covid' : covid_query,
      'prediction' : prediction_query
  }
if __name__ == '__main__':
    app.run() 
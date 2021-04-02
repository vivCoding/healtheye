from flask import Flask
from flask import render_template, Response
import pymongo
#init the client
uri = "Get The link in the discord group"
my_client = pymongo.MongoClient(uri)
#create the database
database = my_client["AIAzure_database"]
#Create collection
covid_data = database['Covid']
prediction_data = database['Prediction']


@app.route("/")
def home_page():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
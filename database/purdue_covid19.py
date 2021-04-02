from tableauscraper import TableauScraper as TS
import pymongo
import json
#init the client
uri = "Get the link in the Discord group"
my_client = pymongo.MongoClient(uri)
#create the database
database = my_client["AIAzure_database"]
#Create collection
covid_data = database['Covid']

url = "https://tableau.itap.purdue.edu/t/public/views/COVIDPublicDashboard/Testing?:isGuestRedirectFromVizportal=y&:embed=y"

ts = TS()
ts.loads(url)
workbook = ts.getWorkbook()
data = {}

for t in workbook.worksheets:
    data[t.name]  = t.data.to_dict('record')
covid_data.insert_one(data) 
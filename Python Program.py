import pandas as pd
import json
import requests

url = 'http://<your url>.azurecontainer.io/score'
key = '<your key>'

spam = {'spam':[1,0,1]}
data = {"data":['PRIVATE! Your 2003 Account Statement for 078','Send me the new number at my work','Free e-book']}

input_data = json.dumps(data)

headers = {'Content-Type':'application/json'}

#for AKS deployment you'd need to the service key in the header as well    
headers = {'Content-Type':'application/json',  'Authorization':('Bearer '+ key)} 

resp = requests.post(uri, input_data, headers=headers)

print("POST to url", uri)
print("input data:", input_data)
print("label:", spam['spam'])
print( resp.text)

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
	import requests, json
	from requests.auth import HTTPBasicAuth
	import cProfile
	import pstats
	import time
	import sys
#data = {
#    "file":open("test1.jpg", "rb"), \
#    "modelId":("", "bce519b9-5484-47da-ab25-b947e5298fa4")
#}
#
#headers = {
#    'accept': 'multipart/form-data'
#}
#
#url = "https://app.nanonets.com/api/v2/ObjectDetection/Model/bce519b9-5484-47da-ab25-b947e5298fa4/LabelFile/"
#r = requests.post(url, headers=headers, files=data, auth=HTTPBasicAuth('ODBgLIipDcqMzkElTA7vrkne8sYjh2mV45k0ar4vhvz', ''))
#json_data=r.json()
#print (json_data['result'][0]['prediction'])
#k=0
#for i in json_data['result'][0]['prediction']:
#    print(json_data['result'][0]['prediction'][k]['label'])


	data = {
	"file":open('./20.jpg', "rb"), \
	"modelId":("", "bce519b9-5484-47da-ab25-b947e5298fa4")
	}
	headers = {
	'accept': 'multipart/form-data'
	}
	url = "https://app.nanonets.com/api/v2/ObjectDetection/Model/bce519b9-5484-47da-ab25-b947e5298fa4/LabelFile/"
	r = requests.post(url, headers=headers, files=data, auth=HTTPBasicAuth('ODBgLIipDcqMzkElTA7vrkne8sYjh2mV45k0ar4vhvz', ''))
	json_data=r.json()
	return str(json_data['result'][0]['prediction'])

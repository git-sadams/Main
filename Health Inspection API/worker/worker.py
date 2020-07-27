from flask import Flask, jsonify
from hotqueue import HotQueue
import json
import redis

rd = redis.StrictRedis(host='redis', port =6379, db=7)
q = HotQueue("queue", host="redis", port=6379, db=15)

austin = []
temp_data={}
temp_data['data'] = []
save = {}
save['data'] = []
def getdata():
	with open('food.txt') as json_file:
		data = json.load(json_file)
		return data
def openlist():
	restaurants = getdata()
	for p in restaurants['data']:
		austin.append(p)
	return'database opened'
def closelist():
	for p in austin:
		save['data'].append(p)
	with open('food.txt', 'w') as outfile:
		json.dump(save,outfile)
	austin.clear()
	temp_data['data'].clear() 
	save['data'].clear()
	return 'database closed'
@q.worker
def do_work(item):
	if item['Command'] == 'Display':
		openlist()
		key = str(item['key'])
		for p in austin:
			temp_data['data'].append(p)
		result = json.dumps(temp_data)
		rd.set(key, result)
		closelist()
		print('task completed')
	if item['Command'] == 'Find':
		openlist()
		x=0
		key = str(item['key'])
		for p in austin:
			if(int(item['Facility ID']) == p['Facility ID']):
				x=1
				temp_data['data'].append(p)
		if(x==1):
			result = json.dumps(temp_data)
		else:
			result = 'Facility ID not Found'
		rd.set(key, result)
		closelist()
		print('task completed')
	if item['Command'] == 'Quality':
		openlist()
		for p in austin:
			if(int(item['Score']) <= int(p['Score'])):
				temp_data['data'].append(p)
		key = str(item['key'])
		result = json.dumps(temp_data)
		rd.set(key, result)
		closelist()
	if item['Command'] == 'Update':	
		openlist()
		key = str(item['key'])
		x=0
		Temp = 0
		for p in austin:
			if(int(item['Facility ID'])== p['Facility ID']):
				Temp=x
			x=x+1
		if (Temp ==0):
			rd.set(key, 'Facility not Found')
		else:
			austin[Temp]["Score"] = int(item["Score"])
			rd.set(key, 'Facility Score Successfully Updated')
		closelist()
	if item['Command'] == 'Zip':	
		key = str(item['key'])
		openlist()
		for p in austin:
			if(int(item['Zip']) == p['Zip Code']):
				temp_data['data'].append(p)
		result = json.dumps(temp_data)
		rd.set(key,result)
		closelist()
	if item['Command'] == 'Zip Score':
		key =str(item['key'])
		x=0
		total = 0
		openlist()
		for p in austin:
			if(int(item['Zip']) == p['Zip Code']):
				x= x+1
				total = total + int(p['Score'])
		if(x == 0):
			result = 'No Restaurants in Selected Zip Code'
		else:
			average = total/x
			result = 'The average of selected zip code is ' + str(average)
		rd.set(key, result)
		closelist()
		print('jobdone')
	if item['Command'] == 'New':
		openlist()
		key = str(item['key'])
		x=0
		restaurant = {
		"Restaurant Name": item['Restaurant Name'],
		"Zip Code" : item['Zip Code'],
		"Inspection Date" : item['Inspection Date'],
		"Score" : item['Score'],
		"Address" : item['Address'],
		"Facility ID" : item['Facility ID'],
		"Process Description" : item['Process Description']
		}
		save['data'].append(restaurant)
		rd.set(key, 'Facility Sucessfully Added')
		closelist()
				
			
print ('worker initialized')

do_work()

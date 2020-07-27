from flask import Flask, jsonify, request
import json
import redis
import uuid
from hotqueue import HotQueue
app = Flask(__name__)

rd = redis.StrictRedis(host = 'redis', port = 6379, db = 7)
q = HotQueue("queue", host = "redis", port = 6379, db =15)
#6095


@app.route('/server_test')
def test():
	return 'Oh thank god it works'
@app.route('/task')
def taskID():
	key = request.args.get('Key')
	result = rd.get(key)
	return result
		
@app.route('/full_list', methods = ['GET'])
def full_list():
	key= uuid.uuid4()
	payload = {
	'key' : key,
	'Command' : 'Display'
	}
	q.put(payload)
	return 'Finding Restaurants, Your key is: '+ str(key)
@app.route('/Find_ID', methods = ['GET'])
def find_ID():
	key=uuid.uuid4()
	ID= request.args.get('ID')
	payload = {
	'key' : key,
	'Command' : 'Find',
	'Facility ID' : ID
	}
	q.put(payload)
	return 'Finding your Restaurants, Your key is: ' + str(key)
@app.route('/quality_check', methods = ['GET'])
def quality_check():
	key= uuid.uuid4()
	Score = request.args.get('Score')
	payload= {
	'key' : key,
	'Command': 'Quality',
	'Score' : Score
	}
	q.put(payload)
	return 'Finding Your Restaurants, your key is : '+ str(key)
@app.route('/update_score', methods = ['PUT'])
def update_score():
	
	key= uuid.uuid4()
	payload = request.get_json(force=True)
	payload.update({'key' : key,})
	payload.update({'Command' : 'Update'})
	q.put(payload)
	return 'Updating Your Restaurant your key is : '+ str(key)
@app.route('/Zipcode', methods = ['GET'])
def Zipcode():
	key= uuid.uuid4()
	Zip = request.args.get('Zip')
	payload= {
	'key' : key,
	'Command' : 'Zip',
	'Zip': Zip
	}
	q.put(payload)
	return 'Finding your Restaurants your key is : '+ str(key)
@app.route('/Zip_Score', methods = ['GET'])
def Zip_Score():
	key= uuid.uuid4()
	Zip = request.args.get('Zip')
	payload = {
	'key' : key,
	'Command' : 'Zip Score',
	'Zip' : Zip
	}
	q.put(payload)
	return 'Finding average score for selected Zipcode, your key is: '+ str(key)
@app.route('/New', methods = ['POST'])
def New():
	key= uuid.uuid4()
	payload = request.get_json(force=True)
	payload.update({'Command' : 'New'})
	payload.update({'key' : key})
	q.put(payload)
	return 'Adding your restaurant your key is : '+ str(key)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')

<<<<USER GUIDE>>>>

FILE DESCRIPTIONS:

<---- means files within above directory>

config: Directory housing the redis configuration file

----redis.conf: configuration information for the redis container

docker-compose-yml: docker compose file to create container for service

READ.md: Project Description text file

SPEC.md: User Guide for service

web: Directory housing the files for the flask container

----app.py: Flask application

----dockerfile: docker set up for flask app

----requirements.txt: requirements for flask app dockerfile

worker: Directory housing the files for the worker container

----dockerfile: docker set up for the worker app

----food.txt: database of 1200 food facilities

----requirements.txt: requirements for worker app dockerfile

----worker.py: worker application


SERVICE ENDPOINTS(All routes are using localhost:5016):

GET /server_test: Tests the server connection to see if user is reaching the database


GET /task: takes The input of a task unique ID to return the result of the task

----parameters: 'Key' = Unique task ID provided when you curl any other route

GET /full_list: Creates a list of all 1200 facilities and gives the key to return it

GET /Find_ID: Gives a key that will return a facility information with the entered Facility ID

----Parameters: 'ID' = Faclility ID of Facility you wish to return

GET /quality_check: Gives a key that will return a list of all facility information above an entered score

----Parameters: 'Score' = Inspection score barrier of facilities you want to return

PUT /update_score: Edits the Inspection score of a chosen facility based on facility ID

----Parameters: Payload must be entered in JSON format as follows: -d '{"Facility ID": "<ID of Chosen Facility>", 
Score:"<updated score of facility>"}'

GET /Zipcode: Gives a key that will return a list of facilities information in a given zipcode

----Parameters: 'Zip' = Zip code of desired area for list

GET /Zip_Score: Gives a key that will return the average inspection score for a given zipcode

----Parameters: 'Zip' = Zip code of deserired area to return average of

POST /New: Creates a new facility item to be added to the database and returns a key to confirm it

----Parameters: Payload must be entered in JSON format as follows: -d '{"Restaurant Name": "<Name>", "Zip Code":
"<Zip Code>", "Inspection Date": "<Date>", "Score": "<Inspection Score>", "Address": "<Address>", "Facility ID":
"<Facility ID>", "Process Description": "<Process Description>"}'

EXAMPLE ROUTES & RESPONSES:

curl -X GET localhost:5016/server_test

response: Oh thank god it works

curl -X GET localhost:5016/task?Key=<unique task key>

response: result depends on task being recoverd but will be the result listed for each route below

curl -X GET localhost:5016/full_list

response: Finding Restaurants, Your key is: <unique task key>

result for task key: list of all facilities in following format starting with: {"data": [{"Facility ID": 10555469, "Inspection Date": "8/18/2017", "Zip Code": "", "Score": 92, "Address": "", "Process Description": "Routine Inspection", "Restaurant Name": "RW - The Finishline Carwash"},...........]}

curl -X GET localhost:5016/Find_ID?ID=10555469

response: Finding your Restaurants, Your key is: <unique task key>

result for task key: {"data": [{"Facility ID": 10555469, "Inspection Date": "8/18/2017", "Zip Code": "", "Score": 92, "Address": "", "Process Description": "Routine Inspection", "Restaurant Name": "RW - The Finishline Carwash"}

curl -X GET localhost:5016/quality_check?Score=99

response: Finding Your Restaurants, your key is : <unique task key>

result for task key: {"data": [{"Facility ID": 10103530, "Inspection Date": "1/16/2019", "Zip Code": 78613, "Score": 100, "Address": "14010 N US 183 HWY\nAUSTIN, TX 78613", "Process Description": "Routine Inspection", "Restaurant Name": "Wanna Play, LLC"}

curl -X PUT localhost:5016/update_score -d '{"Facility ID": "2803692", "Score": "86"}'

response: Updating your Restaurant your key is : <unique task key>

result for task key: Facility Score Successfully Updated

curl -X POST localhost:5016/New -d curl -X POST localhost:5060/New -d {"data": [{"Facility ID": 10103530, "Inspection Date": "1/16/2019", "Zip Code": 78613, "Score": 100, "Address": "14010 N US 183 HWY\nAUSTIN, TX 78613", "Process Description": "Routine Inspection", "Restaurant Name": "Wanna Play, LLC"}

response: adding your restaurant your key is : <unique task key>

result for task key:Facility Sucessfully Added

curl -X GET localhost:5016/Zipcode?Zip=78613

response: Finding your restaurants your key is : <unique task key>

result for task key:list of all of the facilities for that zip code in the following format {"data": [{"Facility ID": 10103530, "Inspection Date": "1/16/2019", "Zip Code": 78613, "Score": 100, "Address": "14010 N US 183 HWY\nAUSTIN, TX 78613", "Process Description": "Routine Inspection", "Restaurant Name": "Wanna Play, LLC"}
]}

curl -X GET localhost:5016/Zip_Score?Zip=78613

response: Finding average score for Selected Zipcode, your key is: <unique task key>

result for task key: The average of selected zip code is 92


DATA ACCESS CHARGE: The users will be able to purchase a data access pass that will give them permission to access the data for 24 hours from time of purchase. During this time they will be enabled to make 2 queries every 5 minutes
(/task queries do not count towards this limit) to prevent data overload


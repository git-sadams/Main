# Locust load tests for Tapis v3 APIs </br>

In order to test the performance of various Tapis v3 services, we have used Locust, a load testing tool. Script in this repo can be modified to test any of Tapis v3 services by changing the tenant, user and service configuration. The script attempts to generate a access token for the user provided in the config file and then uses that token to make service calls for a service to be tested. Please note that the access token life time is about 4 hours and it will be generated once after the tests starts. For example, if testuser needs to run load tests on Streams 'ready' endpoint in dev enviroment, the user would set the config file paramters for the user=testuser, tenant=dev, service=streams and path=/ready in the locust.config.json file. 


## Adjusting Test Settings:  
Edit the /scripts/locust.config.json file to change the settings of the tests based on the tenant you would like to run the tests:
  
* "target": Tenant Base URL including v3
* "Tenant_ID": Tenant to test from, default is master
* "base": Tenant to grab the token from, should match the target except without the v3 added
* "User_ID": May change depending on routes accessed 
* "service": Service to test  
* "path": Tested endpoint/route, required to start with a "/"  
* "Token_user": Username for generating token  
* "Token_pass": Password for generating token  
 
The /scripts/locustfile.py would work without any modifications for GET requests. For performing load tests on POST or PUT requests altering the locustfile.py will be required, refer to the commented out requests within locustfile.py for the format on how to structure said requests. 

## To start the tests run:
docker-compose up

## Go to the web browser and type
http://localhost:8089

You should see a pop up for number of users to simulate and hatch rate. Fill these with fields and start tests

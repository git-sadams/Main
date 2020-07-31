from locust import HttpLocust, TaskSet, task
import os
import json

HERE = os.path.dirname(os.path.abspath(__file__))

def get_credentials():
    config = json.load(open(
        os.path.join(HERE, 'locust.config.json')))
    if config.get('access_token'):
        print('inside get credentials')
        jwt_header = os.environ.get('jwt_header', 'X-Tapis-Token')
        headers = {'Content-type': 'application/json'}
       #jwt_header: config.get('access_token'), 'X-Tapis-tenant':'master', 'X-Tapis-User':'streams'}
       # print(headers)
    else:
        print("Must provide an access_token.")
        raise Exception()
    return headers


headers = get_credentials()
print(headers)

class BasicTaskSet(TaskSet):

#    @task(3)
#    def hello(self):
#        self.client.get('/hello')

    @task(1)
    def tests(self):
        self.client.put('/tokens', data = {"refresh_token":""},headers = headers ,)
        #'projecis/tapis_demo_project/sites/tapis_demo_site/instruments/test', headers=headers)

class BasicTasks(HttpLocust):
    task_set = BasicTaskSet
    min_wait = 5000
    max_wait = 10000

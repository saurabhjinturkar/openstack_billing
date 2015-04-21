import sqlite3
import ceilometerclient.client
import os

class Controller():
    def authenticate(self):
        pass

os.environ['OS_USERNAME']='admin'
os.environ['OS_PASSWORD']='parbhani'
os.environ['OS_TENANT_NAME']='demo'
os.environ['OS_AUTH_URL']='http://localhost:5000/v2.0/'
print os.environ['OS_AUTH_URL']
#cclient = ceilometerclient.client.get_client(2, os_username=admin, os_password=admin, os_tenant_name=Default, os_auth_url=)
cclient = ceilometerclient.client.get_client(2, os_username=os.environ['OS_USERNAME'], os_password=os.environ['OS_PASSWORD'], os_tenant_name=os.environ['OS_TENANT_NAME'], os_auth_url=os.environ['OS_AUTH_URL'])

dict1 = cclient.meters.list()
dict2 = cclient.samples.list()
print dict1
#for a in dict1:
 #   print a

for meter in dict1:
    print cclient.statistics.list(meter.name)

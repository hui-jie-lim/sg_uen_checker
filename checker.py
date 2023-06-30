import sys
import requests

from stdnum.sg import uen

if len(sys.argv) == 1: # default
    limit = 10

if len(sys.argv) == 2: # default
    if isinstance(sys.argv[1],int) and sys.argv[1] > 0: 
        limit = sys.argv[1]
    else:
        limit = 10

if len(sys.argv) > 2: # use default
    limit = 10

limit_str = "&limit="+str(limit)

r = requests.get("https://data.gov.sg/api/action/datastore_search?resource_id=6b5cbfa7-b502-4ce6-875d-dafff7ff04f2"+limit_str)

companies = list(r.json()["result"]["records"])
for coy in companies:
    uen_no = coy["uen"]
    if (uen.validate(uen_no) == uen_no):
        continue

print("all good for", limit, "checks" )

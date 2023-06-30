from stdnum.sg import uen
import requests

limit = 50000  # magic number unfortunately. unable to find a way to stream api/ get all entries at once
limit_str = ""
if limit > 0:
    limit_str = "&limit="+str(limit)

r = requests.get("https://data.gov.sg/api/action/datastore_search?resource_id=6b5cbfa7-b502-4ce6-875d-dafff7ff04f2"+limit_str)

companies = list(r.json()["result"]["records"])
for coy in companies:
    uen_no = coy["uen"]
    if (uen.validate(uen_no) == uen_no):
        continue

print("all good")

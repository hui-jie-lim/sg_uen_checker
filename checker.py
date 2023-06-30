import sys
import requests

from stdnum.sg import uen

# argument processing
if len(sys.argv) == 1: # default
    limit = 10
if len(sys.argv) == 2: 
    limit = sys.argv[1]
limit_str = "&limit="+str(limit)

# source : https://data.gov.sg/dataset/entities-with-unique-entity-number
acra_resource_id = "39201285-b73e-487a-a971-3a12d34ab8d9"
other_resource_id = "5ab68aac-91f6-4f39-9b21-698610bdf3f7" 
acra_errors = 0
other_errors = 0
errors = []
count = 0

def validate(category_name: str, uen_resource_id: str, count: int):
    count = 0
    r = requests.get("https://data.gov.sg/api/action/datastore_search?resource_id="
                    + uen_resource_id
                    + limit_str)
    
    companies = list(r.json()["result"]["records"])
    for coy in companies:
        uen_no = coy["uen"]
        try:
            if uen.validate(uen_no) == uen_no:
                count += 1
        except:
            errors.append(tuple([uen_no, coy["issuance_agency_id"], coy["uen_status"], coy["entity_type"]]))    
 
    print("Total", category_name, "registered validated count", count )
    error_count = len(errors) 
    if error_count == 0:
        print("No errors")
    else:
        print(error_count, category_name, "UEN with errors")

    return error_count


acra_errors = validate("ACRA", acra_resource_id, count)
print("")
other_errors = validate("Other", other_resource_id, count)
print("")
print("Total", acra_errors + other_errors, "UEN with errors")
print(errors)




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
val_errors = []
digit_errors = []
entity_errors = dict()
troublesome_entities = set()
count = 0

alpha_list = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

def validate(category_name: str, uen_resource_id: str):
    val_errors.clear()
    digit_errors.clear()
    entity_errors.clear()

    count = 0
    r = requests.get("https://data.gov.sg/api/action/datastore_search?resource_id="
                    + uen_resource_id
                    + limit_str)
    
    companies = list(r.json()["result"]["records"])

    for coy in companies:

        uen_no = coy["uen"]
        # print(uen_no)
        
        # happy path
        try:  
            if uen.validate(uen_no) == uen_no:
                count += 1
        except:
            val_errors.append(tuple(["ValidationError", uen_no, coy["issuance_agency_id"], coy["uen_status"], coy["entity_type"]]))    

        # misery - digit check
        uen_list = list(uen_no)
        digit_check = set()
        for alpha in alpha_list:
            uen_list[-1] = alpha
            uen_temp = ''.join(uen_list)
            try: 
                uen.validate(uen_temp) 
            except:
                continue
            digit_check.add(alpha)
        if len(digit_check) > 1:
            digit_errors.append(tuple(["DigitCheckError", uen_no, coy["issuance_agency_id"], coy["uen_status"], coy["entity_type"]]))    

        # misery - entity type
        uen_list = list(uen_no)
        entity_count = 0
        if not uen_list[3].isalpha() and not uen_list[4].isalpha():
            continue
        else:
            original_i = uen_list[3]
            original_j = uen_list[4]
            for i in alpha_list:
                for j in alpha_list:
                    uen_list[3] = i
                    uen_list[4] = j
                    uen_temp = ''.join(uen_list)
                    try: 
                        uen.validate(uen_temp) 
                    except:
                        continue
                    if i == original_i and j == original_j:
                        continue
                    entity_count += 1
                    troublesome_entities.add(''.join([i,j]))
        entity_errors[uen_no] = entity_count

    print("Total", category_name, "registered validated count", count )
    error_count = len(val_errors) + len(digit_errors) + len(entity_errors)
    if error_count == 0:
        print("No errors")
    else:
        print("Validation:", len(val_errors), "UEN with errors")
        print("Digit Check", len(digit_errors), "UEN with errors")
        print("Entities Check", len(entity_errors), "UEN with errors")
        print("Total", error_count, category_name, "UEN with errors")

    return error_count


acra_errors = validate("ACRA", acra_resource_id)
print("")
# print("validation error:", val_errors)
# print("digit check error:", digit_errors)
# print("entity error:", entity_errors)
print("troublesome entities:", troublesome_entities)
print("-"*70)


other_errors = validate("Other", other_resource_id)
print("")
# print("validation error:", val_errors)
# print("digit check error:", digit_errors)
# print("entity error:", entity_errors)
print("troublesome entities:", troublesome_entities)



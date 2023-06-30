# requirements

head over to https://github.com/arthurdejong/python-stdnum and clone the repo onto your machine. Alternatively, just use 

    gh repo clone arthurdejong/python-stdnum

Thereafter run the following to install stdnum onto your local machine. Ideally, do this in your virtual environment.  

    cd python-stdnum && python3 setup.py install

# How to run

simply run the following. entries is optional. if not provided, we'll use a default of 100 entries to verify against. 

    python3 checker.py <entries>

# more info on UENs

* R = Registered * D = Deregistered
Reference table: https://www.uen.gov.sg/ueninternet/faces/pages/admin/aboutUEN.jspx

# sources

Current source : https://data.gov.sg/dataset/entities-with-unique-entity-number

Alternate source: https://data.gov.sg/dataset/acra-information-on-corporate-entities

The alternate source list entities from a - z. To use the alternate source, just create new resource id and then pass a name and the resource_id over to the validate function.

    alpha_a_resource_id = "6b5cbfa7-b502-4ce6-875d-dafff7ff04f2" 
    validate("alpha_a", alpha_a_resource_id) 
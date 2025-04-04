import requests
import pandas as pd
import re

def inchi_from_name(CHEMICAL_NAME):
    # Common names are notoriously unreliable chemical identifiers. The InchiKey has an extremely low probability of collision.
    URL = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{CHEMICAL_NAME}/property/InChiKey/TXT"
    response = requests.get(URL)

    if response.status_code == 200:
        inchikey = response.text.strip() 
        return inchikey
    else:
        print(f"Request failed with status code: {response.status_code}")
        return None

def pubchem_cid_from_inchi(INCHI):
    # for work within pubchem we will use compound ids (CIDs)
    cid_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/inchikey/{INCHI}/cids/JSON"
    
    cid_response = requests.get(cid_url)
    if cid_response.status_code == 200:
        cid = cid_response.json()['IdentifierList']['CID'][0]
        return cid
    else:
        print(f"Failed to get CID. Status code: {cid_response.status_code}")
        return None
    
#convenience function...
def pubchem_cid_from_name(CHEMICAL_NAME):
    return pubchem_cid_from_inchi(inchi_from_name(CHEMICAL_NAME))
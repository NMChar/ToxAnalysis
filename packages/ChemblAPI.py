from chembl_webresource_client.new_client import new_client
from urllib.parse import quote
import requests
import pandas as pd

def chemblid_from_inchi(inchi_key):
    molecule = new_client.molecule
    mol = molecule.filter(molecule_structures__standard_inchi_key=inchi_key).only(['molecule_chembl_id'])
    chembl_id = mol[0]['molecule_chembl_id']
    return chembl_id

def chembl_ADME(chembl_id, organism):
    organism = quote(organism)
    # I am hard coding this to fetch me ADME-relevant assays only b/c it's what I will be working with downstream
    base_url = f"https://www.ebi.ac.uk/chembl/api/data/activity?assay_type=A&molecule_chembl_id={chembl_id}&target_organism={organism}&limit=1000&format=json"
    
    all_activities = []
    next_url = base_url

    while next_url:
        response = requests.get(next_url)
        if response.status_code == 200:
            data = response.json()
            activities = data.get("activities", [])
            all_activities.extend(activities)
            next_endpoint = data.get("page_meta", {}).get("next")
            if next_endpoint != None:
                next_url = f"https://www.ebi.ac.uk/{next_endpoint}"
            else:
                break
        else:
            print(f"Request failed with status code {response.status_code} on URL: {next_url}")
            break

    return all_activities

def chembl_tox(chembl_id,):

    base_url = f"https://www.ebi.ac.uk/chembl/api/data/activity?assay_type=T&molecule_chembl_id={chembl_id}&limit=1000&format=json"
    
    all_activities = []
    next_url = base_url

    while next_url:
        response = requests.get(next_url)
        if response.status_code == 200:
            data = response.json()
            activities = data.get("activities", [])
            all_activities.extend(activities)
            next_endpoint = data.get("page_meta", {}).get("next")
            if next_endpoint != None:
                next_url = f"https://www.ebi.ac.uk/{next_endpoint}"
            else:
                break
        else:
            print(f"Request failed with status code {response.status_code} on URL: {next_url}")
            break

    return all_activities

def clean_ADME(adme_assays, types= []):
    df = pd.DataFrame(adme_assays,)[['assay_chembl_id', 'assay_description', 'bao_endpoint', 'target_organism','target_pref_name', 'type', 'units', 'value']]
    return df.loc[df['type'].isin(types)]

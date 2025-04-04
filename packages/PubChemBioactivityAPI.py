import requests
import pandas as pd

def assay_description(aid):
    URL = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/{aid}/description/JSON"
    response = requests.get(URL)

    if response.status_code == 200:
        data = response.json()
        assay_description = data['PC_AssayContainer'][0]['assay']['descr']['description']
        return assay_description
    else:
        print(f"Failed to retrieve assay. HTTP status code: {response.status_code}")
        return None
    
def pubchem_bioactivity_summary(CID):
    URL = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{CID}/assaysummary/JSON"    
    assay_response = requests.get(URL)
    if assay_response.status_code == 200:
        return assay_response.json()
        print(f"Bioactivity assay summary for CID {cid} retrieved.")
    else:
        print(f"Failed to get assay summary. Status code: {assay_response.status_code}")
        return None

def bioactivity_json_to_dframe(data):
    columns = data['Table']['Columns']['Column']
    rows = [row['Cell'] for row in data['Table']['Row']]
    df = pd.DataFrame(rows, columns=columns)
    return df 
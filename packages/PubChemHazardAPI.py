import requests
import os
import json
import re

def hazard_codes(CID):
    URL = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{CID}/JSON?heading=Safety+and+Hazards"
    response = requests.get(URL)
    if response.status_code == 200:
        return response.json()
        print(f"Safety/Hazard summary for CID {cid} retrieved.")
    else:
        print(f"Failed to get assay summary. Status code: {assay_response.status_code}")
        return None
    
# just going to hard code these...https://unece.org/sites/default/files/2023-07/GHS%20Rev10e.pdf Pgs 298-299 for the curious...
with open(os.path.join(os.getcwd(), "hazard_code_definitions.json"), "r") as fin:
    hazard_definitions = json.load(fin)

def extract_ghs_hazard_codes(CID):
    # doing an extraction on pubchem safety & hazard data. In production this should be more cautiously cleaned and vetted with sources of hazard data being recorded.
    URL = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{CID}/JSON?heading=Safety+and+Hazards"
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
    
        h_pattern = re.compile(r"\bH\d{3}\b")
        codes = {}
    
        try:
            info_blocks = data['Record']['Section'][0]['Section'][0]['Section'][0]['Information']
        except (KeyError, IndexError):
            return {}
    
        for entry in info_blocks:
            if entry.get('Name') == 'GHS Hazard Statements':
                ref = entry.get('ReferenceNumber')
                string_markup = entry.get('Value', {}).get('StringWithMarkup', [])
                h_matches = [
                    h for block in string_markup
                    for h in h_pattern.findall(block.get('String', ''))
                ]
                codes[ref] = h_matches
    else:
        print(f"Failed to get hazard codes. Status code: {response.status_code}")

    return codes

def summarize_hazard_codes(codes):
    flat_codes = {code for sublist in codes.values() for code in sublist}
    summary = {'Number of Sources': len(codes), 'Hazard Codes': sorted(flat_codes), 'GHS Definitions' : [hazard_definitions[i] for i in sorted(flat_codes) if i in hazard_definitions.keys()]}
    return summary
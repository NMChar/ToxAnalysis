import requests

def get_cancer_data(dtxsid, api_key):
    url = f"https://api-ccte.epa.gov/hazard/cancer-summary/search/by-dtxsid/{dtxsid}"
    headers = {
        "x-api-key": api_key  # Correct header
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None
    
def get_hazard_data(dtxsid, api_key):
    url = f"https://api-ccte.epa.gov/hazard/search/by-dtxsid/{dtxsid}"
    headers = {
        "x-api-key": api_key  # Correct header
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None
    
def get_dtxsid_from_inchikey(inchikey, api_key):
    url = f"https://api-ccte.epa.gov/chemical/search/equal/{inchikey}"
    headers = {
        "x-api-key": api_key
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()[0]['dtxsid']
        return data
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None
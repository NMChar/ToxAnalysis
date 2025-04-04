import requests
from datetime import datetime, timedelta

def get_pubmed_ids(chemical_name, keywords=[], max_results=10):
    today = datetime.today().strftime('%Y/%m/%d')
    last_year = (datetime.today() - timedelta(days=365)).strftime('%Y/%m/%d')
    
    search_terms = chemical_name + '+' + '+'.join(keywords)

    URL = (
        f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        f"?db=pubmed&term={search_terms}"
        f"&retmax={max_results}"
        f"&retmode=json"
        f"&datetype=pdat&mindate={last_year}&maxdate={today}"
    )

    response = requests.get(URL)
    response.raise_for_status()
    data = response.json()

    return data.get("esearchresult", {}).get("idlist", [])

def get_abstract(pubmed_id):
    URL = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pubmed_id}&retmode=text&rettype=abstract"

    response = requests.get(URL)
    response.raise_for_status()
    data = response.text
    return data
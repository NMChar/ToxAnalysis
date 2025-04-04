def flatten_description(description):
    if isinstance(description, list):
        return " ".join(description)
    return str(description) 

def tox_keyword_hits(description):
    # this is a quick and dirty way of selecting assays for tox relevance
    # would be a prime candidate for LLM enhancement
    keywords = [
        "tcarcinogen", "teratogen", "developmental", "CYP",
        "estrogen", "androgen", "mutagen", "AhR" # receptor implicated w/ dioxins
    ]
    desc = flatten_description(description).lower()
    hits = [kw for kw in keywords if kw.lower() in desc]
    return hits if hits else None

def summarize_assay_data(tox_assays):
    keyword_counts = {}
    for i in tox_assays.keys():
        for j in tox_assays[i]['keywords']:
            if j not in keyword_counts:
                keyword_counts[j] = 1
            else:
                keyword_counts[j] += 1
    return keyword_counts
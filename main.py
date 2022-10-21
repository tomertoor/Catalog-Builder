import mitreattack.attackToExcel.attackToExcel as attackToExcel
import mitreattack.attackToExcel.stixToDf as stixToDf
import json


def parse_tactics(t):
    
    # this is the json we will return
    r: json = {}

    # for each tactic
    for row in t.index:
        str(row)

        j: json = json.loads(t.to_json())
        
        # this is the json for the tactic in the format we want
        row_json: json = {}

        for field in j:
            if field != "ID":
                row_json[field] = j[field][row]
        
        # adding the tactic to r with the tactic ID as the key
        r[j["ID"][row]] = row_json
        
    return r


# download and parse ATT&CK STIX data
data = attackToExcel.get_stix_data("enterprise-attack")

# get Pandas DataFrames for tactics & techniques
tactics_df = stixToDf.tacticsToDf(data)["tactics"]
techniques_df = stixToDf.techniquesToDf(data, "enterprise-attack")["techniques"]

print(parse_tactics(tactics_df[["ID", "name", "last modified", "version"]]))
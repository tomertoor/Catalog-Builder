from os import P_ALL
import mitreattack.attackToExcel.attackToExcel as attackToExcel
import mitreattack.attackToExcel.stixToDf as stixToDf
import json


def parse_df(t):
    
    # this is the json we will return
    r: json = {}

    # for each tactic
    for row in t.index:
        row = str(row)

        j: json = json.loads(t.to_json())
        
        # this is the json for the tactic in the format we want
        row_json: json = {}

        for field in j:
            if field != "ID":
                row_json[field] = j[field][row]
        
        # adding the tactic to r with the tactic ID as the key
        r[j["ID"][row]] = row_json
        
    return r

def main():

    filename = input("enter filename to save to or \'.\' if you dont want to save: ")

    # download and parse ATT&CK STIX data
    data = attackToExcel.get_stix_data("enterprise-attack")

    # get Pandas DataFrames for tactics & techniques
    tactics_df = stixToDf.tacticsToDf(data)["tactics"]
    techniques_df = stixToDf.techniquesToDf(data, "enterprise-attack")["techniques"]

    # parsing tactics techniques and suntechniques
    p_tactics: json = parse_df(tactics_df[["ID", "name", "created", "last modified", "version"]])
    p_techniques: json = parse_df(techniques_df.loc[techniques_df["is sub-technique"] == False][["ID", "name", "created", "last modified", "version", "tactics"]])
    p_sub: json = parse_df(techniques_df.loc[techniques_df["is sub-technique"] == True][["ID", "name", "created", "last modified", "version", "sub-technique of"]])

    # attach subtechniques to techniques
    for technique in p_techniques:
        subtechniques_json = {}
        subtechniques_list = []

        for i in p_sub:
            if p_sub[i]["sub-technique of"] == str(technique):
                subtechniques_json[i] = p_sub[i]
        
        p_techniques[technique]["sub-techniques"] = subtechniques_json


    # attach techniques to tactics
    for tactic in p_tactics:
        techniques_json = {}
        techniques_list = []

        for i in p_techniques:
            if p_tactics[tactic]["name"] in p_techniques[i]["tactics"]:
                techniques_json[i] = p_techniques[i]

        p_tactics[tactic]["techniques"] = techniques_json

    if filename == '.':
        print(json.dumps(p_tactics))
    else:
        f = open(filename, "w")
        f.write(json.dumps(p_tactics))

if __name__ == '__main__':
    main()
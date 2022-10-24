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

                # transform field names
                if field == "last modified":
                    row_json["last_modified"] = j[field][row]
                elif field == "sub-technique of":
                    row_json["sub_technique_of"] = j[field][row]
                else:
                    row_json[field] = j[field][row]


        row_json["name"] = row_json["name"].split(": ")[-1]
        
        # adding the tactic to r with the tactic ID as the key
        r[j["ID"][row] + '-' + j["name"][row].split(": ")[-1]] = row_json
        
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

    # merging the jsons
    final_json = {**p_tactics, **p_techniques, **p_sub}

    if filename == '.':
        print(json.dumps(final_json))
    else:
        f = open(filename, "w")
        f.write(json.dumps(final_json))

if __name__ == '__main__':
    main()
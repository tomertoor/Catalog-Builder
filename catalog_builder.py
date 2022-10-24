from os import P_ALL
import sys
from tabnanny import verbose
import mitreattack.attackToExcel.attackToExcel as attackToExcel
import mitreattack.attackToExcel.stixToDf as stixToDf
import json

helpstr = """
USAGE:
    catalog_builder.py
        run the program normally (in-program prompt)

    catalog_builder.py -h or --help
        help

    catalog_builder.py -p or --print
        print the JSON

    catalog_builder.py <filename>
        save the json to filename
"""

def help():
    print(helpstr)
    return

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
                else:
                    row_json[field] = j[field][row]

        row_json["name"] = row_json["name"].split(": ")[-1]

        if "TA" in j["ID"][row]:
            row_json["type"] = "tactic"
        elif '.' in j["ID"][row]:
            row_json["type"] = "sub-technique"
        else:
            row_json["type"] = "technique"

        # adding the tactic to r with the tactic ID as the key
        r[j["ID"][row] + '-' + j["name"][row].split(": ")[-1]] = row_json

    return r

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            help()
            return
        elif sys.argv[1] == "-p" or sys.argv[1] == "--print":
            filename = '-'
        else:
            filename = sys.argv[1]
    else:
        filename = input("enter filename to save to or \'-\' if you dont want to save: ")

    # download and parse ATT&CK STIX data
    data = attackToExcel.get_stix_data("enterprise-attack")

    # get Pandas DataFrames for tactics & techniques
    tactics_df = stixToDf.tacticsToDf(data)["tactics"]
    techniques_df = stixToDf.techniquesToDf(data, "enterprise-attack")["techniques"]

    # parsing tactics techniques and suntechniques
    p_tactics: json = parse_df(tactics_df[["ID", "name", "created", "last modified", "version"]])
    p_techniques: json = parse_df(techniques_df[["ID", "name", "created", "last modified", "version"]])

    # merging the jsons
    final_json = {**p_tactics, **p_techniques}

    if filename == "-":
        print(json.dumps(final_json))
    else:
        f = open(filename, "w")
        f.write(json.dumps(final_json))
        print("done!")

if __name__ == '__main__':
    main()
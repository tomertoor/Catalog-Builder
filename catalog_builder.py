# from os import P_ALL
import sys
from tabnanny import verbose
# import mitreattack.attackToExcel.attackToExcel as attackToExcel
# import mitreattack.attackToExcel.stixToDf as stixToDf
import json
from urllib.request import urlopen

JSON_URL = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"

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

def parse_json(t):
    # this is the json we will return
    r = []
    # for each tactic
    for element in t:
        if element["type"] == "x-mitre-tactic" or element["type"] == "attack-pattern":
            #type -> url
            #id -> external-referances->external-id
            #name -> name
            #created -> created
            #last modified -> modified
            #depricated -> x_mitre_depracated
            #version -> x_mitre_version
            if element["type"] == "x-mitre-tactic":
                type = "tactic"
            elif element["type"] == "attack-pattern":
                try:
                    if element["x_mitre_is_subtechnique"]:
                        type = "sub_technique"
                    else:
                        type = "technique"
                except:
                    type = "technique"
            
            a = f'{element["external_references"][0]["external_id"]}-{element["name"]}'
            j : json = {}
            try:
                d = element["x_mitre_deprecated"]
            except:
                d = False
            data = {"name":element["name"], "created":element["created"], "last_modified":element["modified"], 
            "version":element["x_mitre_version"], "type":type, "deprecated":d}
            j[a] = data
            r.append(j)
    return r

def main():
    # download and parse ATT&CK STIX data
    # data = attackToExcel.get_stix_data("enterprise-attack")



    res = urlopen(JSON_URL)
    data = json.loads(res.read())


    data = json.dumps(parse_json(data["objects"]))

    f = open("result.json", "w")
    f.write(str(data))
    print("done!")

if __name__ == '__main__':
    main()




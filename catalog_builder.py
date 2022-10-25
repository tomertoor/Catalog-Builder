import json
from urllib.request import urlopen

JSON_URL = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"

T_TACTIC = "x-mitre-tactic"
T_TECHNIQUE = "attack-pattern"

def parse_json(t):
    # this is the json we will return
    r = []

    for element in t:
        # this is to sort out non-tactic or non-technique objects
        if element["type"] == T_TACTIC or element["type"] == T_TECHNIQUE:
            if element["type"] == T_TACTIC:
                type = "tactic"
            elif element["type"] == T_TECHNIQUE:
                try:
                    if element["x_mitre_is_subtechnique"]:
                        type = "sub_technique"
                    else:
                        type = "technique"
                except:
                    type = "technique"
            
            key = f'{element["external_references"][0]["external_id"]}-{element["name"]}'

            value: json = {}

            try:
                d = element["x_mitre_deprecated"]
            except:
                d = False
            
            data = {
                "name": element["name"],
                "created": element["created"],
                "last_modified": element["modified"],
                "version": element["x_mitre_version"],
                "type": type,
                "deprecated": d
                }

            value[key] = data
            r.append(value)
    return r

def main():
    # get the mitre json
    res = urlopen(JSON_URL)

    # parse
    data = json.dumps(parse_json(json.loads(res.read())["objects"]))

    # write
    f = open("result.json", "w")
    f.write(str(data))
    print("done!")

if __name__ == '__main__':
    main()
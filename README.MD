**Catalog builder**

This tool outputs a JSON file or string representing the MITRE ATT&CK enterprise STIX matrix

```USAGE:
    catalog_builder.py
        run the program normally (in-program prompt)

    catalog_builder.py -h or --help
        help

    catalog_builder.py -p or --print
        print the JSON

    catalog_builder.py <filename>
        save the json to filename
```

Dependencies:
1) Att&ck Python Utilities: `pip install mitreattack-python`

Example output (this is a single sub-technique a single technique and a single tactic):

```
{
  "TA0009-Collection": {
    "name": "Collection",
    "created": "17 October 2018",
    "last_modified": "19 July 2019",
    "version": "1.0"
  },
  "T1548-Abuse Elevation Control Mechanism": {
    "name": "Abuse Elevation Control Mechanism",
    "created": "30 January 2020",
    "last_modified": "21 March 2022",
    "version": "1.0",
    "tactics": "Defense Evasion, Privilege Escalation"
  },
  "T1548.002-Bypass User Account Control": {
    "name": "Bypass User Account Control",
    "created": "30 January 2020",
    "last_modified": "19 April 2022",
    "version": "2.0",
    "sub_technique_of": "T1548"
  }
}
```

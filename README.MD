**Catalog builder**

This tool outputs a JSON representing the MITRE ATT&CK enterprise STIX matrix

Dependencies:
1) Att&ck Python Utilities: `pip install mitreattack-python`

Example output (this is the output of a single sub-technique of a single technique of a signle tactic):

{
  'TA0009': {
    'name': 'Collection',
    'created': '17 October 2018',
    'last modified': '19 July 2019',
    'version': '1.0',
    'techniques': {
      'T1557': {
        'name': 'Adversary-in-the-Middle',
        'created': '11 February 2020',
        'last modified': '19 April 2022',
        'version': '2.1',
        'tactics': 'Collection, Credential Access',
        'sub-techniques': {
          'T1557.002': {
            'name': 'Adversary-in-the-Middle: ARP Cache Poisoning',
            'created': '15 October 2020',
            'last modified': '28 July 2021',
            'version': '1.1',
            'sub-technique of': 'T1557'
          }
        }
      }
    }
  }
}

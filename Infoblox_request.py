# Import the required Python modules.
import requests
import json
import getpass
import sys

# Set parameters to access the NIOS WAPI.
url = 'https://gm.example.com/wapi/v1.0/'
id = 'api-test'  # Userid with WAPI access
valid_cert = True  # False if GM uses self-signed certificate

# Prompt for the API user password.
pw = getpass.getpass('Password for user ' + id + ': ')

# Retrieve all CNAME records (up to a max of 5000) in the default DNS view.
dns_view = 'default'
max_results = -5000
req_params = {'view': dns_view,
              '_max_results': str(max_results)}
r = requests.get(url + 'record:cname',
                 params=req_params,
                 auth=(id, pw),
                 verify=valid_cert)
if r.status_code != requests.codes.ok:
    print r.text
    exit_msg = 'Error {} finding CNAME records: {}'
    sys.exit(exit_msg.format(r.status_code, r.reason))
results = r.json()

# For each CNAME record keep track of the canonical name pointed
# to by that record, by adding the canonical name to a Python set.
canonicals = set()
for result in results:
    canonicals.add(result['canonical'])

# Sort the resulting set of canonical names and print them.
for canonical in sorted(canonicals):
    print canonical

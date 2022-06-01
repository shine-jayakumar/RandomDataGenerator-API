
# common.py
# Contains common functions

import json
import random
from response import Response, ResponseMessages


def get_random_records(fname:str, nrecords:int) -> list[dict]:
    """
    Generates and returns random records
    """
    names:dict = None

    with open(fname, 'r') as fh:
        names = json.load(fh)

    firstnames = names['firstnames']
    lastnames = names['lastnames']
    addresses = names['addresses']

    random.shuffle(firstnames)
    random.shuffle(lastnames)
    random.shuffle(addresses)

    records = []

    for fname, lname, address in zip(firstnames[:nrecords], lastnames[:nrecords], addresses[:nrecords]):
        records.append({
            'firstname': fname,
            'lastname': lname,
            'address': address
        })
    return records


def validate_search_params(request_params) -> Response:
    """
    Validates search parameters
    """
    required_params = ('record_id','firstname', 'lastname', 'address')

     # Record Id not present
    if 'record_id' not in request_params:
        return Response(False, ResponseMessages.RecordIDMissing.value)

    # Un-recognized parameter
    for param in request_params:
        if param not in required_params:
            return Response(False, ResponseMessages.InvalidParameters.value)
    
    return Response(True, ResponseMessages.SuccessfulSearch.value)
    

def parse_search_params(request_params) -> dict:
    """
    Parses search parameter
    Returns: dict with param:value
    """
    required_params = ('record_id','firstname', 'lastname', 'address')

    parsed_params:dict = {}
    for param in required_params:
        param_val = request_params.get(param)
        if param_val:
            parsed_params[param] = param_val
    return parsed_params


def get_params_as_string(request):
    """
    Returns paramerts in request.args as a string
    Ex:
        {'firstname':'John', 'lastname'='Smith'} as
        firstname=John&lastname=Smith
    """
    if request.method == 'GET':
        base_url = request.base_url + '?'
        return request.url.replace(base_url, '')
    
    if request.method == 'POST':
        param_list = [f'{key}={val}' for key,val in request.args.items()]
        return '&'.join(param_list)
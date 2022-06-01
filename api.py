
# api.py
# random data generator
# version: v.1
# Generates random firstnames, lastnames, and addresses

# Author: Shine Jayakumar


from flask import Flask, render_template, request
from common import parse_search_params, validate_search_params, get_params_as_string
from common import get_random_records
from persistent import Record
from response import Response, ResponseMessages
from caching import LRUCache

app = Flask(__name__)

cache = LRUCache(maxsize=500)

@app.route('/')
@app.route('/generate')
@app.route('/generate/')
def version():
    return render_template('usage.html')
    

# Endpoint: /generate/<int:nrec>
# Generates random records
@app.route('/generate/<int:nrec>', methods=['GET'])
def generate_records(nrec):
    
    # max 10000 records
    if nrec > 10000:
        return Response(False, ResponseMessages.RequestExceedMaxRecords.value).get_response()
    
    random_records = get_random_records('records.json', nrec)
    record = Record()
    record.save_to_db(random_records)
    response = record.get_records().get_response()
    return response


# Endpoint: /search
# Search functionality with record_id, firstname, lastname, and address
@app.route('/search', methods=['GET','POST'])
def search():
    response_validity = validate_search_params(request.args)

    # Invalid search parameters
    if not response_validity.success:
        return response_validity.get_response()
    
    # param:val pair -> dict
    parsed_search_params = parse_search_params(request.args)

    # firstname=John&lastname=Smith
    params_as_string = get_params_as_string(request)

    # check in cache
    if cache.exists(params_as_string):
        search_result = cache.get(params_as_string)
        return Response(
            True,
            ResponseMessages.SuccessfulSearch.value,
            parsed_search_params['record_id'],
            search_result).get_response()
    
    # Instantiate record for searching
    record = Record(parsed_search_params['record_id'], search=True)

    # If the supplied record_id doesn't exist
    if not record.table_is_valid:
        return Response(False, ResponseMessages.RecordIDDoNotExist.value).get_response()

    search_result = record.search_db(parsed_search_params)

    # store in cache
    cache.set(params_as_string, search_result)
    
    return Response(
        True,
        ResponseMessages.SuccessfulSearch.value,
        record.tablename,
        search_result).get_response()


if __name__ == '__main__':
    app.run(debug=True)

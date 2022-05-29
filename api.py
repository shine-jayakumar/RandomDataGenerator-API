
# api.py
# random data generator
# version: v.1
# Generates random firstnames, lastnames, and addresses

# Author: Shine Jayakumar



from flask import Flask, render_template, request
from common import parse_search_params, validate_search_params, get_random_records
from persistent import Record
from response import Response, ResponseMessages


app = Flask(__name__)

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
    validity_response = validate_search_params(request.args)

    # Invalid search parameters
    if not validity_response.success:
        return validity_response.get_response()

    parsed_search_params = parse_search_params(request.args)
    # Instantiate record for searching
    record = Record(parsed_search_params['record_id'], search=True)

    # If the supplied record_id doesn't exist
    if not record.table_is_valid:
        return Response(False, ResponseMessages.RecordIDDoNotExist.value).get_response()

    search_result = record.search_db(parsed_search_params)

    return search_result.get_response()


if __name__ == '__main__':
    app.run(debug=True)

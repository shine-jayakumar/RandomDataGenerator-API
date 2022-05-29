
# response.py
# Contains Response class and Response messages

from enum import Enum
from flask import jsonify

class ResponseMessages(Enum):
    RecordIDMissing:str = "Record ID missing"
    InvalidParameters:str = "Invalid parameters"
    RecordsGenerated:str = "Records generated"
    SuccessfulSearch:str = "Successful search"
    RecordIDDoNotExist:str = "Record Id does not exist"
    RequestExceedMaxRecords:str = "Request exceeded max records of 10000"

class Response:
    def __init__(self, success: bool, msg: str, record_id: str = None, records: list[dict] = []):
        self.success:bool = success
        self.msg:str = msg
        self.record_id:str = record_id
        self.records:list[dict] = records
    
    def get_response(self):
        """
        Jsonified response
        """
        return jsonify({
            'record_id': self.record_id,
            'records': self.records,
            'success': self.success,
            'msg': self.msg
        })
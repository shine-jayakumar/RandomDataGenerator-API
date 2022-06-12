# persistent.py
# Function and class to allow persistence

from sqlalchemy import create_engine, inspect, MetaData, Table, Column, Integer, String
from sqlalchemy import and_, text, select
from uuid import uuid4
from constants import *
from response import Response


ENGINE = create_engine(SQLALCHEMY_CONNECT_URI)

class Record:

    def __init__(self, tablename: table = None, search:bool = False) -> None:
        self.record_id = str(uuid4())
        self.search = search
        self.records:list[dict] = []
        # use tablename if specified or generate one
        self.dbname = DBNAME
        self.tablename:str = tablename or self.record_id
        self.table_is_valid = False
        self.connect_uri:str = SQLALCHEMY_CONNECT_URI
        self.engine:str = None
        self.conn:str = None
        self.meta:str = None
 
        self._init_connection()


    def _init_connection(self) -> None:
        self.engine = ENGINE
        self.conn = self.engine.connect()
        self.inspect = inspect(self.engine)
        self.meta = MetaData(bind=self.engine)

        # # create table if not exist
        # if not self.engine.dialect.had_table(self.engine, self.tablename):
        self.user = Table(
            self.tablename,
            self.meta,
            Column('id', Integer, primary_key=True),
            Column('firstname', String(20), nullable=False),
            Column('lastname', String(20), nullable=False),
            Column('address', String(100), nullable=False),
            Column('id', Integer, primary_key=True))
        
        # create table only if user is not searching
        if not self.search:
            self.meta.create_all()
            self.table_is_valid = True
        # validate table
        self.validate_table()

    def validate_table(self) -> None:
        """
        Checks if table exists or not and sets 'table_is_valid' flag
        """
        # if self.inspect.has_table(self.tablename, schema='dbo'): # works on mssql
        # schema was changed for mysql
        if self.inspect.has_table(self.tablename, schema=self.dbname):
            self.table_is_valid = True
    
    def save_to_db(self, records: list[dict]) -> None:
        """
        Saves randomly generated records to db
        """
        self.records = records
        self.conn.execute(self.user.insert(), self.records)
    
    def search_db(self, parsed_search_params) -> list[dict]:
        query = select([self.user.c.firstname, self.user.c.lastname, self.user.c.address])
        conditions = []

        # if firstname, lastname, address is specified
        if len(parsed_search_params) > 1:
            # keys -> firstname, lastname, address
            for key,val in parsed_search_params.items():
                if key != 'record_id':
                    conditions.append(f"LOWER({key})='{val.lower()}'")

            # append conditions to query with AND statement
            query = select([
                self.user.c.firstname, 
                self.user.c.lastname, 
                self.user.c.address]).where(text(' AND '.join(conditions)))

        # get raw sql results - list[tuple]
        raw_search_result = self.conn.execute(query).fetchall()
        # get results as list[dict]
        processed_search_results = self.process_search_results(raw_search_result)
        return processed_search_results
        
    
    def process_search_results(self, raw_search_result:list[tuple]) -> list[dict]:
        """
        Processed the raw search result from db (list[tuple])
        Returns: list[dict]
        """
        processed_search_results = []
        for record in raw_search_result:
            processed_search_results.append({
                'firstname': record[0],
                'lastname': record[1],
                'address': record[2]
            })
        return processed_search_results

    def get_records(self) -> Response:
        """
        Returns a Response with tablename/record_id and records
        """
        if self.records:
            return Response(True, 'Records generated', self.tablename, self.records)

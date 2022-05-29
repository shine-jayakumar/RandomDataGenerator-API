# constants.py
# Contains contstants

from typing import NewType
import os

table = NewType('DBTable', str)
dbconnection = NewType('DBConnection', str)

SQLALCHEMY_CONNECT_URI = os.environ.get('SQLALCHEMY_MYSQL_URI')
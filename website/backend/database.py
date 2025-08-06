import MySQLdb
import os
from dotenv import load_dotenv

load_dotenv('./.env')

# Database Credentials
SERVER = os.getenv('server')
USERNAME = os.getenv('user')
PASSWORD = os.getenv('pwd')
DATABASE = os.getenv('db_name')

# List of databases.
ACCESS_RIGHTS_TABLE = "access_rights_table"
APPLICATION_STATISTICS_TABLE = "application_statistics_table"
DOCUMENT_TABLE = "document_table"
ENTITY_TABLE = "entity_table"
REDACTION_TABLE = "redaction_table"
USERS_TABLE = "users_table"
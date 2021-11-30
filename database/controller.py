import MySQLdb
import os

# See following webpage for instructions on dotenv:
# https://dev.to/jakewitcher/using-env-files-for-environment-variables-in-python-applications-55a1
from dotenv import load_dotenv
load_dotenv()

# Loads environment variables from .env file.
host = os.environ.get('340DBHOST')
user = os.environ.get('340DBUSER')
password = os.environ.get('340DBPW')
db = os.environ.get('340DB')

def connect_to_database(host=host, user=user, password=password, db=db):
    '''
    Connects to a database and returns a database objects
    '''
    db_connection = MySQLdb.connect(host,user,password,db)
    return db_connection


def execute_query(db_connection = None, query = None, query_params = ()):
    '''
    executes a given SQL query on the given db connection and returns a Cursor object
    db_connection: a MySQLdb connection object created by connect_to_database()
    query: string containing SQL query
    returns: A Cursor object as specified at https://www.python.org/dev/peps/pep-0249/#cursor-objects.
    You need to run .fetchall() or .fetchone() on that object to actually access the results.
    '''

    if db_connection is None:
        print("No connection to the database found! Have you called connect_to_database() first?")
        return None

    if query is None or len(query.strip()) == 0:
        print("Query is empty! Please pass a SQL query in query")
        return None

    print(f'Executing {query} with {query_params}');
    # Create a cursor to execute query. Why? Because apparently they optimize execution by retaining a reference according to PEP0249
    cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)

    '''
    params = tuple()
    #create a tuple of paramters to send with the query
    for q in query_params:
        params = params + (q)
    '''
    #TODO: Sanitize the query before executing it!!!
    cursor.execute(query, query_params)
    # No changes will be committed to database unless query is executed.
    db_connection.commit();
    return cursor

if __name__ == '__main__':
    print('Executing a sample query')
    db = connect_to_database()
    params = (None,'Nathan', 'MacTest')
    query = '''INSERT INTO `Employees` (`departmentID`, `firstName`, `lastName`) VALUES (%s, %s, %s);'''
    results = execute_query(db, query, params)
    print(f'Printing results of {query}')

    for result in results.fetchall():
        print(result)

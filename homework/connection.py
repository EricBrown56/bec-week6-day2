import mysql.connector
from mysql.connector import Error

# Database connection parameters

db_name = 'fitness_center'
db_user = 'root'
db_password = 'Groovin'
db_host = 'localhost'

def connection():
    '''Function to establish a connection to the database'''
    try:
        conn = mysql.connector.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password
        )
        if conn.is_connected():
            print('Connected to MySQL database')
            return conn
    except Error as e:
        print(e)
        return None
   
import mysql.connector
import os

''' handler function to return connection to our search db'''
def get_connection():
    connection = mysql.connector.connect(
    host = os.environ.get('HOST_NAME'),
    user = os.environ.get('USER_NAME'),
    password = os.environ.get('PASSWORD'),
    database = os.environ.get('DB_NAME')
    )
    return connection
# import libraries
import psycopg2
import sys

from psycopg2.extras import RealDictCursor
# create function to connect mysql database
def ConnectDatabase():
    conn = None
    try:
        conn = psycopg2.connect(
        host='localhost', 
        user='postgres', 
        password='G0t0hell',
        database='fastapi',
        cursor_factory=RealDictCursor)
    except:
        print("Error: ", sys.exc_info())
    finally:
        return conn
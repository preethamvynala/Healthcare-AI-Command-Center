import psycopg
import os


DATABASE_URL=os.getenv(
   "DATABASE_URL"

)



def get_connection():

    conn=psycopg.connect(
        DATABASE_URL
    )

    return conn

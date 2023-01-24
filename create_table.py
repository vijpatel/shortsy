#!/usr/bin/python

import psycopg2
from connect import connect


def create_tables():
    delete_table_query = '''DROP TABLE IF EXISTS urls CASCADE;'''
    create_table_query = '''CREATE TABLE urls (
    id SERIAL PRIMARY KEY,
    custom_url TEXT,
    original_url TEXT NOT NULL,
    date_created TIMESTAMP NOT NULL DEFAULT LOCALTIMESTAMP,
    clicks INTEGER NOT NULL DEFAULT 0); '''
    conn = None
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute(delete_table_query)
        cur.execute(create_table_query)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
if __name__ == '__main__':
    create_tables()
#!/usr/bin/python
import psycopg2
import os

def connect():
    conn = None
    try:
        # params = config()
        #DATABASE_URL = "postgres://retdvwko:a60qYJRwjOhai8D5kUJqtaKKQoq4qijU@kashin.db.elephantsql.com/retdvwko"
        # DATABASE_URL = "postgres://wckmbyrjnvnvjj:1e954cf7932cfa6b36b5f0da1bb3c7e86faa25770bade84c1ebbdde8edb1009a@ec2-3-211-221-185.compute-1.amazonaws.com:5432/d60ju4dsfltm0"
        # conn = psycopg2.connect(**params)
        # DATABASE_URL = os.environ.get('DATABASE_URL')
        DATABASE_URL = "postgres://urlshortener_i9yg_user:7hwP6NnziD95a3YWLToSJhZw1pa8V59h@dpg-cf7mj62rrk0e2aqdrdc0-a.oregon-postgres.render.com/urlshortener_i9yg"
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            return conn
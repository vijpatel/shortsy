import psycopg2
from connect import connect
from flask import flash


def insert_url(original_url, custom_url = None):
    try:
        conn = connect()
        cur = conn.cursor()
        postgres_insert_query = """ INSERT INTO "public"."urls" (original_url,custom_url) VALUES (%s,%s) RETURNING id"""
        record_to_insert = (original_url,custom_url)
        cur.execute(postgres_insert_query, record_to_insert)
        last_id = cur.fetchone()[0]
        conn.commit()
        count = cur.rowcount
        if count > 0:
            flag = True
        else:
            flag = False
    except (Exception, psycopg2.Error) as error:
        flag = False
    finally:
        if conn:
            cur.close()
            conn.close()
            return flag,last_id
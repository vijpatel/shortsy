import psycopg2
from connect import connect
from hashids import Hashids
from flask import flash

def fetch_url(id = 0, short_url = None):
	try:
		connection = connect()
		cursor = connection.cursor()
		postgreSQL_select_Query = "SELECT id,original_url,clicks FROM urls WHERE id = %s OR custom_url = %s"
		data = (id,short_url)
		cursor.execute(postgreSQL_select_Query,data)
		count = cursor.rowcount
		url_records = cursor.fetchall()
		if url_records:
			original_url = url_records[0][1]
			index = url_records[0][0]
			clicks = url_records[0][2]
		else:
			original_url = ""
			index = 0
			clicks = 0
	except (Exception, psycopg2.Error) as error:
		flash('Something went wrong. Please try again later')
	finally:
		if connection:
			cursor.close()
			connection.close()
			return original_url,index,clicks
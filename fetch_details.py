import psycopg2
from connect import connect
from hashids import Hashids
from flask import flash

def fetch(id = 0, short_url = None):
	try:
		connection = connect()
		cursor = connection.cursor()
		postgreSQL_select_Query = "SELECT * FROM urls WHERE id = %s OR custom_url = %s"
		data = (id,short_url)
		cursor.execute(postgreSQL_select_Query,data)
		count = cursor.rowcount
		url_records = cursor.fetchall()
		if url_records:
			original_url = url_records[0][2]
			for record in url_records:
				data = {
				'original_url' : record[2],
				'date' : record[3],
				'clicks' : record[4]
				}
		else:
			data = {}
	except (Exception, psycopg2.Error) as error:
		flash('Something went wrong. Please try again later')
	finally:
		if connection:
			cursor.close()
			connection.close()
			return data
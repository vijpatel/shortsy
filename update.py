import psycopg2
from connect import connect
from hashids import Hashids

def update_clicks(id,clicks):
	try:
		connection = connect()
		cursor = connection.cursor()
		query = "UPDATE urls SET clicks = %s WHERE id = %s"
		data = (clicks,id)
		cursor.execute(query,data)
	except (Exception, psycopg2.Error) as error:
		print(error)
	finally:
		if connection:
			connection.commit()
			cursor.close()
			connection.close()

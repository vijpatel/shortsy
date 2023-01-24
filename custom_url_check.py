import psycopg2
from create_hash import decode

def check(custom_url):
	data = decode(custom_url)
	if data:
		return False
	else:
		return True
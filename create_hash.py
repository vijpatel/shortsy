from fetch_details import fetch
from fetch_url import fetch_url
from hashids import Hashids

def encode(id):
	hashids = Hashids(min_length=4, salt='tHiSiSaSeCrEtKeY')
	encoded_string = hashids.encode(id)
	return encoded_string
def decode(encoded_string,only_url = False):
	hashids = Hashids(min_length=4, salt='tHiSiSaSeCrEtKeY')
	decoded_id = hashids.decode(encoded_string)
	if not decoded_id:
		if only_url:
			url,index,clicks = fetch_url(short_url = encoded_string)
			return url,index,clicks
		else:
			data = fetch(short_url = encoded_string)
			return data
	else:
		if only_url:
			url,index,clicks = fetch_url(id = decoded_id)
			return url,index,clicks
		else:
			data = fetch(id = decoded_id)
			return data
from transports import get_transport
from transports import TransportConnetionError

def get_id():
	return "000"

def check():
	try:
		with get_transport('ssh') as ssh_transport:
			i, o, e = ssh_transport.exec("[ -f /testfile ] && echo '1' || echo '2'")
			return o.read()[0] - 48
	except TransportConnetionError as e:
		print(str(e))
		return 4
	except Exception as e:
		print(str(e))
		return 5
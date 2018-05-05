#!/usr/bin/env python3

import paramiko

class UnknownTransport(Exception):
	""" unknown transport exception """
	def __init__(self, expression, message):
		self.expression = expression
		self.message = message

class TransportError(Exception):
	""" file or command dose not exist exception """
	def __init__(self, expression, message):
		self.expression = expression
		self.message = message

class TransportConnetionError(Exception):
	""" transport connection error exception """
	def __init__(self, expression, message):
		self.expression = expression
		self.message = message


class SSHClient:
	""" ssh transport """
	def __init__(self, host, port, login, password):
		self.host 		= host
		self.port 		= port
		self.login 		= login
		self.password 	= password
		self.client = paramiko.SSHClient()
		self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		try:
			self.client.connect(hostname=host,username=login,password=password,port=port)
		except Exception as e:
			raise TransportConnetionError(host, str(e))

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, exc_traceback):
		pass

	def __del__(self):
		self.client.close()

	def close(self):
		self.client.close()

	def exec(self, command):
		i, o, e = self.client.exec_command(command)
		err = e.read()
		if err: 
			raise TransportError(command, err.decode('utf-8'))
		return i, o, e

	def get_file(self, path, mode='rb'):
		sftp = self.client.open_sftp()
		localpath = '/tmp/test.data'
		try:
			data = sftp.file(path, mode=mode).read()
		except Exception as e:
			raise TransportError(path, str(e))
		finally:
			sftp.close()
		return data

def get_connection(transport_name, host, port, login, password):
	avalible_transports = ['ssh']
	if transport_name not in avalible_transports:
		raise UnknownTransport(transport_name, "unknown transport")
	return SSHClient(host, port, login, password)

if __name__ == '__main__':

	try:
		with get_connection('ssh', 'localhost', 22022, 'root', 'pwd') as sshclient:
			i,o,e = sshclient.exec('ls')
			#i,o,e = sshclient.exec('ls-la')
			res = o.read().decode('utf-8')
			print(res, end='')
			print(sshclient.get_file('file.txt').decode('utf-8'), end='')
			#print(sshclient.get_file('/etc/passw'))

	except UnknownTransport as e:
		print('UnknownTransport expression')
		print(e.message, e.expression)
	except TransportError as e:
		print('TransportError expression')
		print(e.message, e.expression)
	except TransportConnetionError as e:
		print('TransportConnetionError')
		print(e.message, e.expression)
	except Exception as e:
		print('UnknownException')
		print(str(e))
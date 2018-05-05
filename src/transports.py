#!/usr/bin/env python3

import paramiko
import json

#config data
_config = None

def get_config():
	"""import config from _config.json file"""
	global _config
	if not _config:
		with open('env.json', 'r') as f:
			#TODO: add checking for config file existing
			_config = json.load(f)
	return _config

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

#TODO: add elementar checking. this look like students handmade =(
def get_transport( transport_name
	              , host=None
	              , port=None
	              , login=None
	              , password=None):
	"""instans transport object"""
	avalible_transports = ['SSH']
	transport_name = transport_name.upper()
	if transport_name not in avalible_transports:
		raise UnknownTransport(transport_name, "unknown transport")

	if not host: host = get_config()['host']
	if not port: port = get_config()['transports'][transport_name]['port']
	if not login: login = get_config()['transports'][transport_name]['login']
	if not password: password = get_config()['transports'][transport_name]['password']

	return SSHClient(host, port, login, password)
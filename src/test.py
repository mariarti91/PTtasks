#!/usr/bin/env python3

import pytest

from transports import *

def test_getTransportException():
	with pytest.raises(UnknownTransport):
		get_transport('sh', 'localhost', 22022, 'root', 'pwd')

def test_createSSHTransportException():
	with pytest.raises(TransportConnetionError):
		get_transport('ssh', 'localhost', 2222, 'root', 'pwd')

def test_createSSHTransport():
	get_transport('ssh', 'localhost', 22022, 'root', 'pwd')

def test_execCommand():
	with get_transport('ssh', 'localhost', 22022, 'root', 'pwd') as client:
		i,o,e = client.exec('ls')
		assert o.read().decode('utf-8') == 'file.txt\n'

def test_execCommandException():
	with pytest.raises(TransportError):
		with get_transport('ssh', 'localhost', 22022, 'root', 'pwd') as client:
			i,o,e = client.exec('ls-la')

def test_getFile():
	with get_transport('ssh', 'localhost', 22022, 'root', 'pwd') as client:
		data = client.get_file('file.txt')
		assert data.decode('utf-8') == 'test\n'

def test_getFileException():
	with pytest.raises(TransportError):
		with get_transport('ssh', 'localhost', 22022, 'root', 'pwd') as client:
			data = client.get_file('fil.txt')

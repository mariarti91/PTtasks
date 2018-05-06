#!/usr/bin/env python3

import os
import importlib
from reportdb import add_control
from reportdb import get_scandata

if __name__ == '__main__':
	files = [f.split('.')[0] for f in os.listdir('./scripts') if os.path.isfile(os.path.join("./scripts", f))]
	for file in files:
		module = importlib.import_module("scripts.{}".format(file))
		add_control(module.get_id(), module.check())

	for row in get_scandata():
		print(row)
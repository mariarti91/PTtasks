#!/usr/bin/env python3

import os
import importlib

if __name__ == '__main__':
	files = [f.split('.')[0] for f in os.listdir('./scripts') if os.path.isfile(os.path.join("./scripts", f))]
	for file in files:
		module = importlib.import_module("scripts.{}".format(file))
		print(module.check())


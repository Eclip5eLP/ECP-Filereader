### --- PENUMBRA --- ###
##  Made by Eclip5e   ##
##  ©Penumbra Games   ##
### ---------------- ###

import math
import re, sys, os
import random
import string
import json
from pathlib import Path
from penumbra import Penumbra
from datetime import datetime

pen = Penumbra()

class ecpreader:

	# Vars
	version = "0.2.1"
	net = "Python"
	pdef = "P3nEncrypt3d"
	CMD = {}

	# Command Line Parameter options
	CMD["read"] = "-r"
	CMD["make"] = "-m"
	CMD["help"] = "-h"

	def __init__(self):
		pass

	# Read file
	def read(self, file):
		if not Path(file).is_file():
			return False

		# Read file
		f = open(file, "r")
		text = f.read()
		f.close()

		# Get file encryption password
		passlen = int(text[:3])
		passw = text[3:passlen + 3]
		fpass = pen.decrypt(passw, self.pdef)
		content = text[passlen + 3::]

		# Decrypt Contents
		content = pen.decrypt(content, fpass).split("\n", 5)

		# Data types
		if int(content[3]) == 1:
			try:
				content[4] = json.loads(content[4]);
			except:
				print("Failed to load data as json! Loaded plaintext instead")

		return content

	# Make file
	def make(self, file, body):
		# Data types
		try:
			json.loads(body)
			types = 1
		except:
			types = 0
		
		# Prepare vars
		timestamp = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
		enc = self.id_generator(random.randint(9,15))
		header = [self.version, self.net, timestamp, enc, types]
		passw = pen.encrypt(header[3], self.pdef)
		passlen = ('00' + str(len(passw)))[-3:]

		# Combine Data
		_res = str(header[0]) + "\n" + str(header[1]) + "\n" + str(header[2]) + "\n" + str(header[4]) + "\n" + body
		_res = str(passlen) + passw + pen.encrypt(_res, header[3])

		# Write Output
		f = open(file, "w")
		f.write(_res)
		f.close()

		return _res

		# Generate random ID/Password for each file
	def id_generator(self, size=9, chars=string.ascii_uppercase + string.digits):
		return ''.join(random.choice(chars) for _ in range(size))

# Command Line
reader = ecpreader()
if len(sys.argv) >= 3 and sys.argv[0] == os.path.basename(__file__):
	# Get Parameters
	cy_read = pen.isParam(reader.CMD["read"])
	cy_make = pen.isParam(reader.CMD["make"])
	if cy_read != -1:
		cfile = sys.argv[cy_read + 1]
	elif cy_make != -1:
		cfile = sys.argv[cy_make + 1]

	# Read file CMD
	if cy_read != -1 and sys.argv[cy_read + 1] != "":
		try:
			ret = reader.read(cfile)
			if ret == False:
				print("File not found")
			else:
				print(ret)
		except:
			print("Filetype not supported")
	# Make file CMD
	elif cy_make != -1 and sys.argv[cy_make + 1] != "":
		ret = reader.make(cfile, sys.argv[cy_make + 2])

		# Write Output
		f = open(cfile, "w")
		f.write(ret)
		f.close()

		print("Done")
	else:
		print("error: Invalid argument '{}'".format(sys.argv[1]))
elif len(sys.argv) == 1:
	# No Parameters
	pass
elif pen.isParam(reader.CMD["help"]) != -1:
	# Syntax Help
	print('Syntax:\necpreader.py <' + reader.CMD["read"] + '/' + reader.CMD["make"] + '> <file> (data)\n\n' + reader.CMD["read"] + '    Read file\n' + reader.CMD["make"] + '    Make file')
else:
	print('Invalid Syntax')
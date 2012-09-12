# -*- coding: UTF-8 -*-


import sys
import webapp2
import os
import tempfile
import shutil

# para Python 2.6 o inferior, utilizamos unittest2
if sys.hexversion < 0x2070000:
    import unittest2 as unittest
else:
    import unittest

import main

class classTester(unittest.TestCase):

	def setUp(self):
		self.old_dir = os.path.abspath(os.curdir) # save old directory
		self.cwd = tempfile.mkdtemp() # new current working directory
		os.chdir(self.cwd)

	def tearDown(self):
		os.chdir(self.old_dir)
		shutil.rmtree(self.cwd)

	#Copia archivo datos.json en directorio temporal, para pruebas con BD.
	def crearBD(self):
		original = str(self.old_dir) + "/datos.json"
		new = str(self.cwd) + "/datos.json" 
		shutil.copyfile(original, new)
		
	def test_getSinBD(self):
		request = webapp2.Request.blank('/')
		response = request.get_response(main.app)
		self.assertEqual(response.status_int, 404)
		self.assertEqual(response.body, '')

	def test_getConBD(self):
		self.crearBD()
		request = webapp2.Request.blank('/')
		response = request.get_response(main.app)
		self.assertEqual(response.status_int, 200)
		self.assertEqual(response.headers['Content-Type'], 'application/json')
		




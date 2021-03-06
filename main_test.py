# -*- coding: UTF-8 -*-

import sys
import webapp2
import os
import tempfile
import shutil
import json

# para Python 2.6 o inferior, utilizamos unittest2
if sys.hexversion < 0x2070000:
    import unittest2 as unittest
else:
    import unittest

import main

class classTesterNoFunc(unittest.TestCase):

	def setUp(self):
		self.old_dir = os.path.abspath(os.curdir) # save old directory
		self.cwd = tempfile.mkdtemp() # new current working directory
		os.chdir(self.cwd)

	def tearDown(self):
		os.chdir(self.old_dir)
		shutil.rmtree(self.cwd)

	#Copia archivo datos.json en directorio temporal, para pruebas con BD.
	def crearBD(self):
		self.original = str(self.old_dir) + "/datos.json"
		self.new = str(self.cwd) + "/datos.json" 
		shutil.copyfile(self.original, self.new)
		
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

	def test_postJSONSinBD(self):
		if os.path.isfile("datos.json") == False:
			f = open("datos.json", 'w+')
			request = webapp2.Request.blank('/')
			request.method = 'POST'
			request.body = 'msj=prueba'
			self.assertEqual(request.POST['msj'], 'prueba')
			obj = {'msj' : request.POST['msj']}
			f.write(json.dumps(obj))
			f.close()
			response = webapp2.Request.blank('/').get_response(main.app)
			self.assertEqual(response.headers['Content-Type'], 'application/json')

	def test_postNoJSONSinBD(self):
		if os.path.isfile("datos.json") == False:
			f = open("datos.json", 'w+')
			request = webapp2.Request.blank('/')
			request.method = 'POST'
			request.body = 'pruebaTxt'
			f.write(request.body)
			f.close()
			f2 = open('datos.json', 'r')
			self.assertEqual(request.body, f2.read())
			request2 = webapp2.Request.blank('/')
			response = request2.get_response(main.app)
			self.assertEqual(response.headers['Content-Type'], 'text/html; charset=utf-8')
			
	def test_postJSONConBD(self):
		self.crearBD()
		request = webapp2.Request.blank('/')
		request.method = 'POST'
		request.body = 'msj=prueba'
		self.assertEqual(request.POST['msj'], 'prueba')
		self.assertEqual(request.get_response(main.app).headers['Content-Type'], 'application/json')

	def test_postNoJSONConBD(self):
		self.crearBD()
		request = webapp2.Request.blank('/')
		request.method = 'POST'
		request.body = 'pruebaTxt'
		data = json.loads(self.readFile())
		data['mensajes'] = str(data['mensajes']) + ', ' + request.body 
		self.assertEqual(data['mensajes'][-9:], 'pruebaTxt')

	def readFile(self):
		f = open("datos.json", 'r')
		temp = f.read()
		return temp

class classTesterFunc(unittest.TestCase):

	def setUp(self):
		self.old_dir = os.path.abspath(os.curdir) # save old directory
		self.cwd = tempfile.mkdtemp() # new current working directory
		os.chdir(self.cwd)
		print self.cwd

	def tearDown(self):
		os.chdir(self.old_dir)
		shutil.rmtree(self.cwd)

	#Copia archivo datos.json en directorio temporal, para pruebas con BD.
	def crearBD(self):
		self.original = str(self.old_dir) + "/datos.json"
		self.new = str(self.cwd) + "/datos.json" 
		shutil.copyfile(self.original, self.new)

	def test_JSON(self):
		self.crearBD()
		request = webapp2.Request.blank('/') # Get inicial
		response = request.get_response(main.app)
		request.method = 'POST'
		request.body = 'msj=prueba' # Post de prueba
		response = request.get_response(main.app)
		data = json.loads(self.readFile())
		self.assertEqual(request.POST['msj'], data['added']) # Se compara para confirmar que se haya anadido

	def readFile(self):
		f = open("datos.json", 'r')
		temp = f.read()
		return temp





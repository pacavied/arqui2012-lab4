import webapp2
import json
import cgitb
import os.path
cgitb.enable()

class Index(webapp2.RequestHandler):
	def get(self):
		data = []
		if os.path.isfile("datos.json"):
			data = json.loads(self.readFile())
			self.response.write(json.dumps(data))
			self.response.headers['Content-Type'] = 'application/json'
		else:
			self.response.set_status(404)

	def readFile(self):
		f = open("datos.json", 'r')
		temp = f.read()
		return temp

class Index2(webapp2.RequestHandler):

	def post(self):
		data = []
		data = json.loads(self.readFile())
		f = open("datos.json", 'w')
		data['added'] = self.request.POST['message']
		f.write(json.dumps(data))
		self.response.write(json.dumps(data))
		self.response.headers['Content-Type'] = 'application/json'

	def readFile(self):
		f = open("datos.json", 'r')
		temp = f.read()
		return temp

app = webapp2.WSGIApplication([('/', Index),('/post*', Index2),], debug=True)

def main():
	from paste import httpserver
	httpserver.serve(app, host='0.0.0.0', port='8080')

if __name__ == '__main__':
	main()


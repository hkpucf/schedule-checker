from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import json
import Cache
import Fetcher
import Scheduler

PORT = 80

def isInt(value):
	try:
		int(value)
		return True
	except ValueError:
		return False

class Handler(SimpleHTTPRequestHandler):
	def do_GET(self):
		params = self.path.split('/')
		params = params[1:]

		# Response header
		self.protocol_version = 'HTTP/1.1'
		self.send_response(200, 'OK')
		self.send_header('Content-type', 'application/json')
		self.send_header('Access-Control-Allow-Origin', '*')
		self.end_headers()

		# Validate paramiters
		error = False
		if(len(params) != 5):
			error = True

		for item in params:
			if(not isInt(item)):
				error = True
				break

		if(error):
			response = [
				["path", params],
				["year", "int"],
				["month", "int"],
				["date", "int"],
				["start_time", "int"],
				["end_time", "int"]
			]
			self.wfile.write(bytes(json.dumps(response)))
			return

		# Create the response
		try:
			scheduleList = Cache.readCache(params[0], params[1], params[2])
		except IOError:
			html = Fetcher.fetch_html(int(params[0]), int(params[1]), int(params[2]), int("0830"), int("2200"))
			scheduleList = Fetcher.parseHTML2List(html)
			Cache.saveCache(params[0], params[1], params[2], scheduleList)

		response = Scheduler.filterTable(scheduleList, int(params[3]), int(params[4]))

		# Write the response
		self.wfile.write(bytes(json.dumps(response)))
		return

httpd = HTTPServer(("0.0.0.0", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()

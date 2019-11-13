from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException
import re
import Cache
import Fetcher
import Scheduler

app = Flask(__name__)

@app.route('/<int:year>/<int:month>/<int:date>/<int:start_time>/<int:end_time>')
def searchRoom(year, month, date, start_time, end_time):
	# Create the response
	try:
		scheduleList = Cache.readCache(year, month, date)
	except IOError:
		html = Fetcher.fetch_html(int(year), int(month), int(date), int("0830"), int("2200"))
		scheduleList = Fetcher.parseHTML2List(html)
		Cache.saveCache(year, month, date, scheduleList)

	response = Scheduler.filterTable(scheduleList, int(start_time), int(end_time))

	# Write the response
	res = jsonify(response)
	res.mimetype = 'application/json'
	res.headers['Access-Control-Allow-Origin'] = '*'
	return res

@app.route('/<int:year>/<int:month>/<int:date>/<string:room>')
def showRoom(year, month, date, room):
	if(not re.match('^[a-zA-Z]{1,2}\\d+[a-zA-Z]?$', room)):
		return jsonify(
				errMsg='Invalid room'
			), 500

	try:
		scheduleList = Cache.readCache(year, month, date)
	except IOError:
		html = Fetcher.fetch_html(int(year), int(month), int(date), int("0830"), int("2200"))
		scheduleList = Fetcher.parseHTML2List(html)
		Cache.saveCache(year, month, date, scheduleList)

	response = Scheduler.selectRoom(scheduleList, room)
	res = jsonify(response)
	res.mimetype = 'application/json'
	res.headers['Access-Control-Allow-Origin'] = '*'
	return res

@app.errorhandler(404)
def errHandler(error):
	return jsonify(
			errMsg='Invalid API path'
		), 500

@app.errorhandler(HTTPException)
def handle_exception(e):
	return jsonify(
			code=e.code,
			name=e.name,
			description=e.description
		), e.code

app.run(host='0.0.0.0', port=80)

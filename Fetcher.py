import requests
import re
from lxml import html as HTMLParser
import csv

def convertTime(time):
	result = (time / 100 - 8) * 2
	result += time % 100 / 30
	result = 1 if (result < 1) else result
	result = 29 if (result > 29) else result
	return result

def getCredential():
	try:
		with open(".env", "r") as file:
			username = file.readline().replace('\r', '').replace('\n', '')
			password = file.readline().replace('\r', '').replace('\n', '')
			return (username, password)
	except IOError:
		return ("", "")

def fetch_html(year, month, day, start, end):
	requests.packages.urllib3.disable_warnings()
	requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'
	try:
		requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += 'HIGH:!DH:!aNULL'
	except AttributeError:
		pass

	with requests.Session() as session:
		session.request("GET", "https://www40.polyu.edu.hk/cdoirbs/index.jsp")

		(username, password) = getCredential()

		session.request(
			"POST",
			"https://www40.polyu.edu.hk/cdoirbs/authenUser.do",
			params=[
				("userId", username),
				("userPassword", password)
			]
		)

		res = session.request(
			"POST",
			"https://www40.polyu.edu.hk/cdoirbs/booking/populateDate.do",
			json={
				"id": 1,
				"method": "populateAcadWeekDay",
				"params": [
					str(year) + "-" + str(month) + "-" + str(day)
				]
			},
			headers={
				"Content-Type": "application/json-rpc"
			}
		)

		res = res.json()

		session.request(
			"POST",
			"https://www40.polyu.edu.hk/cdoirbs/enquireRoomBookingInfo.do",
			params=[
				("showResult", True),
				("enquiryRoom", ""),
				("query.roomStatus", 0),
				("query.roomNoCtrl", "S"),
				("query.roomNo", ""),
				("query.campus", "*"),
				("query.minCapacity", 1),
				("query.maxCapacity", 999),
				("query.furniture", "*"),
				("query.semester", "*"),
				("query.strDateRangeStart", str(day) + "-" + str(month) + "-" + str(year)),
				("query.strDateRangeEnd", str(day) + "-" + str(month) + "-" + str(year)),
				("query.acadWeekStart", res["result"]["weekNo"]),
				("query.acadWeekEnd", res["result"]["weekNo"]),
				("query.weekDayStart.dayCode", res["result"]["weekDay"]),
				("query.weekDayEnd.dayCode", res["result"]["weekDay"]),
				("query.timeSlotStart", convertTime(start)),
				("query.timeSlotEnd", convertTime(end) - 1),
				("query.skipNonAcadDate", True),
				("subjActvCtrl", "S"),
				("query.actvCode", ""),
				("query.subjCode", ""),
				("query.Lecturer", ""),
				("query.showMyDeptOnly", False)
			]
		)

		res = session.request("GET", "https://www40.polyu.edu.hk/cdoirbs/popUpDailyReport.do")

		tokenPattern = re.compile("name=\"struts\\.token\" value=\"([a-zA-z\\d]+)\"")
		match = tokenPattern.search(res.content.decode('utf-8'))
		token = match.group(1)

		res = session.request(
			"POST",
			"https://www40.polyu.edu.hk/cdoirbs/printDailyReport.do",
			params=[
				("struts.token.name", "struts.token"),
				("struts.token", token),
				("query.sortColumn", "ROOM_NO"),
				("query.sortOrder", "ASC"),
				("loop", "0")
			]
		)

		return res.content.decode('utf-8')

def parseHTML2List(html):
	resultList = []
	parser = HTMLParser.fromstring(html)
	rows = iter(parser.xpath("//tr[@class='report_body']/parent::table//tr"))
	for row in rows:
		values = [col.text.strip() if isinstance(col.text, str) else col.text for col in row]
		if(len(values) > 1):
			resultList.append(values)
	return resultList

if __name__ == "__main__":
	html = fetch_html(2018, 10, 16, int("1830"), int("2130"))
	with open("untitled.html", "w") as file:
		file.write(html)

	scheduleList = parseHTML2List(html)
	with open('data.csv', 'wb') as file:
		wr = csv.writer(file, quoting=csv.QUOTE_ALL)
		for row in scheduleList:
			wr.writerow(row)

import csv
import os

def readCache(year, month, day):
	try:
		with open("cache/" + str(int(year)) + "-" + str(int(month)) + "-" + str(int(day)) + ".csv", 'r') as csvfile:
			resultList = list(csv.reader(csvfile, delimiter=',', quotechar='"'))
			return resultList
	except IOError as e:
		raise e

def saveCache(year, month, day, cacheList):
	if not os.path.exists("./cache/"):
		os.makedirs("./cache")
	with open("cache/" + str(int(year)) + "-" + str(int(month)) + "-" + str(int(day)) + ".csv", 'w') as csvfile:
		wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
		for row in cacheList:
			wr.writerow(row)

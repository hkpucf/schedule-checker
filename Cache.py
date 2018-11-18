import csv
import os

def readCache(year, month, day):
	with open("cache/" + str(int(year)) + "-" + str(int(month)) + "-" + str(int(day)) + ".csv", 'rb') as csvfile:
		resultList = list(csv.reader(csvfile, delimiter=',', quotechar='"'))
		return resultList

def saveCache(year, month, day, cacheList):
	if not os.path.exists("./cache/"):
		os.makedirs("./cache")
	with open("cache/" + str(int(year)) + "-" + str(int(month)) + "-" + str(int(day)) + ".csv", 'wb') as csvfile:
		wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
		for row in cacheList:
			wr.writerow(row)

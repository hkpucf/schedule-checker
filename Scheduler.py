import csv

ROOM_NO_COL = 1
CAPACITY_COL = 2
FURNITURE_COL = 3
TIME_COL = 7

def compareRow(row1, row2):
	if(row1[ROOM_NO_COL] < row2[ROOM_NO_COL]):
		return 1
	elif(row1[ROOM_NO_COL] > row2[ROOM_NO_COL]):
		return -1
	elif(row1[TIME_COL] < row2[TIME_COL]):
		return 1
	elif(row1[TIME_COL] > row2[TIME_COL]):
		return -1
	else:
		return 0

def mergeTable(left, right):
	leftCount = 0
	rightCount = 0
	resultList = []
	while(leftCount < len(left) and rightCount < len(right)):
		if(compareRow(left[leftCount], right[rightCount]) > 0):
			resultList.append(left[leftCount])
			leftCount += 1
		else:
			resultList.append(right[rightCount])
			rightCount += 1

	while(leftCount < len(left)):
		resultList.append(left[leftCount])
		leftCount += 1

	while(rightCount < len(right)):
		resultList.append(right[rightCount])
		rightCount += 1

	return resultList

def mergeSortTable(table):
	if(len(table) <= 1):
		return table

	left = mergeSortTable(table[:int(len(table) / 2)])
	right = mergeSortTable(table[int(len(table) / 2):])

	return mergeTable(left, right)

def getFreeTimeslot(table):
	freeTimeslotTable = []
	if(len(table) < 1):
		return freeTimeslotTable
	room = table[0][ROOM_NO_COL]
	capacity = table[0][CAPACITY_COL]
	furniture = table[0][FURNITURE_COL]
	start = table[0][TIME_COL][:5]
	end = table[0][TIME_COL][8:]

	for i in range(1, len(table)):
		if(table[i][ROOM_NO_COL] == room and table[i][TIME_COL][:5] == end):
			end = table[i][TIME_COL][8:]
		else:
			freeTimeslotTable.append([room, capacity, furniture, start + " - " + end])
			room = table[i][ROOM_NO_COL]
			capacity = table[i][CAPACITY_COL]
			furniture = table[i][FURNITURE_COL]
			start = table[i][TIME_COL][:5]
			end = table[i][TIME_COL][8:]

	freeTimeslotTable.append([room, capacity, furniture, start + " - " + end])

	return freeTimeslotTable

def filterTable(table, start, end):
	table = mergeSortTable(table[1:])

	freeTimeslotTable = getFreeTimeslot(table)

	newTable = []

	for row in freeTimeslotTable:
		if((int(row[3][:2]) * 100 + int(row[3][3:5])) <= start and (int(row[3][8:10]) * 100 + int(row[3][11:13])) >= end):
			newTable.append(row)

	return newTable

def selectRoom(table, room):
	table = mergeSortTable(table[1:])

	freeTimeslotTable = getFreeTimeslot(table)

	newTable = []

	for row in freeTimeslotTable:
		if(row[0] == room):
			newTable.append(row)

	return newTable

if __name__ == "__main__":
	with open("data.csv", 'rb') as csvfile:
		table = list(csv.reader(csvfile, delimiter=',', quotechar='"'))
	table = filterTable(table, int("1830"), int("2000"))

	for row in table:
		print(row[0] + "\t" + row[1] + "\t" + row[2] + "\t" + row[3])

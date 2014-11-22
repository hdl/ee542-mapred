import sys
import csv

results = open('YelpResults.csv','wb')
writer = csv.writer(results,delimiter = ',')
stations = open('v2.csv','r')
reader = csv.reader(stations, delimiter = ',')
list = open('full_list.csv','r')
list_reader = csv.reader(list, delimiter = ',')
write_line = ['Station Name', #0
			'Station Address', #1
			'City',#2
			'Zip', #3
			'Phone', #4
			'Hours', #5
			'Charger Network', #6
			'Latitude', #7
			'Longitude', #8
			'Score', #9
			'Businesses'] #10
writer.writerow(write_line) #write header
for s_line in reader:
	#stationName = s_line[1]
	#stationAddr = s_line[2]
	#stationCity = s_line[4]
	#stationZip = s_line[6]
	#stationPhone = s_line[8]
	#stationHours = s_line[12]
	#stationLat = s_line[24]
	#stationLng = s_line[25]
	#stationNetwrk = s_line[21]
	found = 0
	write_line[0] = s_line[1]
	write_line[1] = s_line[2]
	write_line[2] = s_line[4]
	write_line[3] = s_line[6]
	write_line[4] = s_line[8]
	write_line[5] = s_line[12]
	write_line[6] = s_line[21]
	write_line[7] = s_line[24]
	write_line[8] = s_line[25]
	list.seek(0) #reset to beginning of file
	for line in list_reader:
		if(s_line[24] == line[0]): #found match with coordinates
			write_line[9] = line[2]
			write_line[10] = line[3]
			found = 1
			break
	if (found == 0): #zero score from EMR
		write_line[9] = "0"
		write_line[10] = ""
	writer.writerow(write_line)
results.close()
stations.close()
list.close()			

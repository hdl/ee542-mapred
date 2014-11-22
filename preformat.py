import sys
import csv

full_list = open('full_list.csv','wb')
writer = csv.writer(full_list,delimiter = ',')
write = ["lat","long","score","businesses"]
for x in range(0,7):
	file_name = 'part-0000%d'%x
	temp = open(file_name,'r')
	for line in temp:
		line = line.strip()
		temp_line = line.split("\t",2)
		if(len(temp_line) == 1):
			continue
		write[0],write[1] = temp_line[0].replace("(","").replace(")","").split(", ")
		write[2] = temp_line[1]
		write[3] = temp_line[2]
		writer.writerow(write)
		#full_list.write(",".join(temp_line)+"\n")
	temp.close()
full_list.close()
#!/usr/bin/env python
import sys

businessCounts = dict()
#for counting number of businesses
businessNames = dict()
#for keeping string of business names

for line in sys.stdin:
	line = line.strip()
	input_key,input_value = line.split('\t', 1)
	if(input_key in businessCounts):
		businessCounts[input_key] += 1
		businessNames[input_key] = businessNames[input_key]+", "+input_value
		#concatenate the names into a list
	else:
		businessCounts[input_key] = 1
		businessNames[input_key] = input_value

for key in businessCounts:
	print key+"\t%d\t"%(businessCounts[key])+businessNames[key]+"\n"
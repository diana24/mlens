#!/usr/bin/python

from operator import itemgetter
import sys

current_user = 0
mvr_list = ""

for line in sys.stdin:
	line = line.strip()
	parts = line.split(",")
	user_id = parts[0]
	movie_id = parts[1]
	rating = parts[2]

	if(current_user == 0):
		current_user = user_id
		res = movie_id + ',' + rating + ' '
		mvr_list = mvr_list + res
	elif(current_user == user_id):
		res = movie_id + ',' + rating + ' '
		mvr_list = mvr_list + res
	else:
		print('%s\t%s') % (current_user, mvr_list)
		current_user = user_id
		mvr_list = ""
		res = movie_id + ',' + rating + ' '
		mvr_list = mvr_list + res
		

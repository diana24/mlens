#!/usr/bin/env python

import sys

for line in sys.stdin:
	line=line.strip()
	parts = line.split("::")
	user_id = parts[0]
	movie_id = parts[1]
	rating = parts[2]
	print '%s,%s,%s' % (user_id,movie_id,rating)

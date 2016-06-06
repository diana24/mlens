#!/usr/bin/python

fin = open("ratingslarge.dat")
fout = open("ratings.dat", "wb")
counter = 0
for line in fin:
    if not (counter % 10 == 0):
        fout.write(line)
    counter = counter + 1
fin.close()
fout.close()

#!/usr/bin/python

fin = open("ratingslarge.dat")
fout = open("ratings.dat", "wb")
counter = 0
for line in fin:
    if counter % 4 == 0:
        fout.write(line)
    counter = counter + 1
fin.close()
fout.close()

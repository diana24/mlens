#!/usr/bin/python

import sys

# Read data
def read_similarities(fname):
    allratings = []
    with open(fname) as fin:
        for line in fin:
            end = line.find(']')
            # ignore lines that don't have at least 1 ]
            if end > 0:
                pair = line[:end+1]
                rating = line[end+2:]
                # Safety, http://lybniz2.sourceforge.net/safeeval.html
                aa = eval(pair, {'__builtins__':None}, {})
                bb = eval(rating, {'__builtins__':None}, {})
                bb[0] = round(bb[0], 3)
                cc = [aa, bb]
                #print cc
                allratings.append(cc)
    return allratings

def find_similar(movie_id, allr):
    res = []
    for i in allr:
        other_movie_id = -1
        if movie_id == i[0][0]:
            other_movie_id = i[0][1]
        if movie_id == i[0][1]:
            other_movie_id = i[0][0]
        if other_movie_id >= 0:
            res.append([other_movie_id, i[1][0], i[1][1]])
    return res

def uimain():
    allr = read_similarities(sys.argv[1])
    print find_similar(int(sys.argv[2]), allr)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Usage:", sys.argv[0], " similarities_file movie_id"
        sys.exit(1)
    uimain()

#!/usr/bin/python

import sys

def read_movielist(fname):
    allmovies = []
    with open(fname) as fin:
        for line in fin:
            fields = line.split('::')
            if len(fields) >= 3:
                movie_id = int(fields[0])
                movie_name = fields[1]
                movie_genre = fields[2]
                allmovies.append((movie_id, movie_name, movie_genre))
    return allmovies

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

def find_similar(movie_id, threshold, allr):
    res = []
    for i in allr:
        other_movie_id = -1
        if movie_id == i[0][0]:
            other_movie_id = i[0][1]
        if movie_id == i[0][1]:
            other_movie_id = i[0][0]
        if other_movie_id >= 0:
            if (i[1][0] - threshold) >= 0:
                res.append([other_movie_id, i[1][0], i[1][1]])
    return res

def movie_name_by_id(movie_id, movies):
    for rec in movies:
        if rec[0] == movie_id:
            return rec[1]
    return "Unknown Movie"

def find_similar_pretty(movie_id, threshold, allr, movies):
    tmp = find_similar(movie_id, threshold, allr)
    if len(tmp) == 0:
        print "No movie is similar to", movie_name_by_id(movie_id, movies), "[", movie_id, "]"
        return
    print "Movies similar to", movie_name_by_id(movie_id, movies), "[", movie_id, "]"
    for sim in tmp:
        print movie_name_by_id(sim[0], movies), "[", sim[0], "]", "similarity", sim[1], "by", sim[2], "people"


def uimain():
    allr = read_similarities(sys.argv[2])
    allm = read_movielist(sys.argv[1])
    threshold = 0.8
    if len(sys.argv) > 3:
        threshold = float(sys.argv[4])
    find_similar_pretty(int(sys.argv[3]), threshold, allr, allm)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Usage:", sys.argv[0], "movie_file similarities_file movie_id similarity_threshold (optional, default 0.8)"
        sys.exit(1)
    uimain()

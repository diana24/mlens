#!/usr/bin/python

import sqlite3
import sys

fin = open(sys.argv[1])

def convert_similarities(fname, dboutname):
    dbout = sqlite3.connect(dboutname)
    dbout.text_factory = str
    dbout.execute("create table if not exists similarities (left integer, right integer, similarity real, count integer, catleft text, catright text)")
    dbout.execute("create index if not exists leftindex on similarities(left)")
    dbout.execute("create index if not exists rightindex on similarities(right)")
    dbout.execute("delete from similarities")
    dbout.execute("insert into similarities (left, right, similarity, count) values (1, 2, 3.5, 4)")
    i = 0
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
                dbout.execute("insert into similarities (left, right, similarity, count) values (?, ?, ?, ?)", (aa[0], aa[1], bb[0], bb[1]))
                if i % 100 == 0:
                    dbout.commit()
                    print "s", i
                i = i + 1
    dbout.commit()
    dbout.close()

def convert_movies(fname, dboutname):
    dbout = sqlite3.connect(dboutname)
    dbout.text_factory = str
    dbout.execute("create table if not exists movies (id integer primary key, title text, category text)")
    dbout.execute("delete from movies")
    i = 0
    with open(fname) as fin:
        for line in fin:
            s = line.split("::")
            if len(s) >= 3:
                dbout.execute("insert into movies (id, title, category) values (?, ?, ?)", (int(s[0]), s[1], s[2].rstrip('\r\n')))
            if i %100 == 0:
                dbout.commit()
            i = i + 1
    dbout.commit()
    dbout.close()

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print "Usage:", sys.argv[0], " movie_file similarities_file destination_db"
        sys.exit(1)
    convert_similarities(sys.argv[2], sys.argv[3])
    convert_movies(sys.argv[1], sys.argv[3])
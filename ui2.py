#!/usr/bin/python

import sqlite3
import sys

def load_movie_list(dbconn):
    res = []
    for row in dbconn.execute("select id, title, category from movies"):
        res.append(row)
    return res

def movie_name_by_id(movs, id):
    for m in movs:
        if m[0] == id:
            return m[1]
    return "Unknown movie"

def load_similarities(dbconn, movie_id, threshold, check_left):
    res = []
    sql = "select %s, similarity, count from similarities where %s=? and similarity>=?" % ("right" if check_left else "left", "left" if check_left else "right")
    for row in dbconn.execute(sql, (movie_id, threshold)):
        res.append(row)
    return res

def ui2_main():
    if len(sys.argv) < 3:
        print "Usage:", sys.argv[0], "dbfile movie_id [threshold] (default 0.8)"
        sys.exit(1)
    conn = sqlite3.connect(sys.argv[1])

    # Because Les Miserables has an accent and I'm not in the mood to do unicode magic
    conn.text_factory = str

    # Find similar movies
    threshold = 0.8
    if len(sys.argv) > 3:
        threshold = float(sys.argv[3])
    movie_id = int(sys.argv[2])
    results = load_similarities(conn, movie_id, threshold, True)
    results = results + load_similarities(conn, movie_id, threshold, False)

    # Sort by number of ratings, descending
    results.sort(key=lambda rec: rec[2], reverse=True)

    # Load movie data
    movs = load_movie_list(conn)

    # Get rid of db connection
    conn.close()

    if len(results) == 0:
        print "No movie is similar to", movie_name_by_id(movs, movie_id), "[", movie_id, "]"
        return
    print "======================================================================="
    print "Movies similar to", movie_name_by_id(movs, movie_id), "[", movie_id, "]"
    print "======================================================================="
    for sim in results:
        print movie_name_by_id(movs, sim[0]), "[", sim[0], "]", "similarity", sim[1], "by", sim[2], "people"


if __name__ == "__main__":
    ui2_main()
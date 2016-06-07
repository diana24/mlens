#!/usr/bin/python

import sys
import json

def read_movies(fname, movie_list):
    allmovies = {}
    with open(fname) as fin:
        for line in fin:
            fields = line.split('::')
            if len(fields) >= 3:
                movie_id = int(fields[0])
                if movie_id in movie_list:
                    movie_name = fields[1]
                    movie_genre = fields[2].strip().split("|")
                    allmovies[movie_id] = (movie_name, movie_genre)
    return allmovies

def read_similarities(fname, movie_id, threshold):
    movies = [movie_id]
    ratings = [(0, 0)]
    with open(fname) as fin:
        for line in fin:
            pair, rating = line.strip().split('], ', 1)
            pair = json.loads(pair + ']')
            if pair[0] != movie_id:
                #print("Id: %s != %s" % (pair[0], movie_id))
                continue

            rating = json.loads(rating)
            if rating[0] < threshold:
                #print("Id: %s threshold %s < %s" % (movie_id, rating[0], threshold))
                continue
            movies.append(pair[1])
            ratings.append((rating[0], rating[1]))

    allratings = {
        'movies': movies,
        'ratings': ratings,
    }

    return allratings

# Sort by score, number of ratings, then similarity
# And in REVERSE
def smart_cmp(x, y):
    # Score goes first
    if x[3] < y[3]:
        return 1
    elif x[3] > y[3]:
        return -1
    # No of ratings second
    if x[2] < y[2]:
        return 1
    elif x[2] > y[2]:
        return -1
    # Similarity third
    if x[1] < y[1]:
        return 1
    elif x[1] > y[1]:
        return -1
    return 0


def show_similar(movie_id, similarities, movies_dict):
    print("Movie %s Genres: %s is similar to:" % (movies_dict[movie_id][0], movies_dict[movie_id][1]))
    m = []
    for i in range(len(similarities["movies"])):
        id = similarities["movies"][i]
        if id == movie_id:
            continue
        score = 0
        for g in movies_dict[movie_id][1]:
            if g in movies_dict[id][1]:
                score += 1
        if score < 1:
            continue

        m.append((id, similarities["ratings"][i][0],  similarities["ratings"][i][1], score))



        #sorted_similar_movies = sorted(sorted(sorted(m, key=lambda x : x[1]), key=lambda x : x[3]), key=lambda x : x[2])

    sorted_similar_movies = sorted(m, cmp=smart_cmp)

    for movie in sorted_similar_movies:
        id = movie[0]
        print("%s Similarity %.2f by %s people. Score: %d" % (movies_dict[id][0], movie[1], movie[2], movie[3]))




def uimain():
    threshold = 0.8
    if len(sys.argv) > 4:
        threshold = float(sys.argv[4])
    movie_id = int(sys.argv[3])
    similarities = read_similarities(sys.argv[2], movie_id, threshold)
    #print similarities
    movies_dict = read_movies(sys.argv[1], similarities['movies'])
    #print movies_dict
    show_similar(movie_id, similarities, movies_dict)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Usage:", sys.argv[0], "movie_file similarities_file movie_id similarity_threshold (optional, default 0.8)"
        sys.exit(1)
    uimain()

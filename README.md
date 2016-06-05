# Project: Movie Similarities
Implementation of a Movie Recommendation System using MapReduce/SVD. Data used from MovieLens database: <http://grouplens.org/datasets/movielens/>

## MovieLens data structure
<http://files.grouplens.org/papers/ml-1m-README.txt>
- ratings.dat : Contains user IDs, movie IDs, ratings on 5 star scale and time stamp.

    userid::movieid::rating::timestamp
  
    - userid ranges from 1 to 6040
    - movieid ranges from 1 to 3952
    - rating is made on a five-star discrete scale (whole-star rating only) 
    - timestamp is in seconds.

- movies.dat : Contains movie IDs, titles and genres.

     movieID::title::genres

    Titles are movie titles and genres are pipe-separated and are selected from the following genres: Action, Adventure, Animation, Children’s, Comedy, Crime, Documentary, Drama, Fantasy, Film-Noir, Horror, Musical, Mystery, Romance, Sci-Fi, Thriller, War, Western

- users.dat : Contains user IDs, genders, ages, occupations and zip-codes.

    userid::gender::age::occupation::zip-code

    - gender is M or F
    - age is categorized as 1, 18, 25, 35,45, 50, 56. The meanings are: 
        - 1: <18 
        - 18: 18-24 
        - 25: 25-34 
        - 35: 35-44 
        - 45: 45-49 
        - 50: 50-55 
        -  56 is 56+.
    - occupation is one of these:
        - 0: other
        - 1: academic/educator
        - 2: artist
        - 3: clerical/admin
        - 4: college/grad student
        - 5: customer service 
        - 6: doctor/health care 
        - 7: executive/managerial
        - 8: farmer
        - 9: homemaker
        - 10: K-12 student
        - 11: lawyer
        - 12: programmer
        - 13: retired
        - 14: sales/marketing
        - 15: scientist 
        - 16: self-employed 
        - 17: technician/engineer
        - 18: tradesman/craftsman
        - 19: unemployed
        - 20: writer


## Singular Value Decomposition
Process small data sample (1Mb) from MovieLens with SVD from python for baseline results comparison.
Use pyrecsys (http://ocelma.net/software/python-recsys/build/html/algorithm.html).
For sparse matrix scipy package can be an alternative.

## MapReduce
### Running code
Starting from Cloudera image run:

    sudo easy_install mrjob
    sudo yum install numpy scipy
    python ./mlens.py m-small/ratings.dat

To run on HADOOP:

    tar -czvf mlens.tgz m-small/ correlations.py
    python mlens.py m-small/ratings.dat --python-archive mlens.tgz -r hadoop

### MapReduce Jobs description
1. Initial data arranging

    - Map: Emit  User_ID  (Movie_ID, Rating)
    - Reduce: For each User_ID pair all their (Movie_ID, Rating)
    
2. Matching Pairs

    - Map: Emit(Movie_ID, Movie_ID) (Rating, Rating) from the reducer output in Job 1 for all User_ID pairs
    - Reduce: For multiple (Movie_ID, Movie_ID) pairs calculate rating avg/similarity

3. Interpret Results

    - Map: Emit (Movie_ID Movie_ID_compared) (Similarity, Count) from the reducer output in Job 2
    - Reducer: Reduce multiple Movie_ID and sort Movie_ID (Movie_ID_comparable_1, Movie_ID_comparable_2) (similarity average?)


## Ideas: 
http://cdac.in/index.aspx?id=ev_hpc_movie-recommend-mr1

Leave aside test set to evaluate results (with R).

## Resources:
- Creating HADOOP Jobs with python: https://pythonhosted.org/mrjob/guides/writing-mrjobs.html
- Datasets: http://grouplens.org/datasets/movielens/

## Project Participants
- Diana Minzat  - MOC2
- Andrei “Torp” Cojocaru - MOC2
- Nicolae Pavel - MOC2




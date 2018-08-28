import psycopg2

def insert_person(name):
    
    '''insert a string of a person's name to the people_index. 
    The database is formatted to accept a lower case string of first name, last initial
    example 'nick  g' '''
    conn = psycopg2.connect('dbname = boardgames user = postgres')
    cur = conn.cursor()
    cur.execute(("INSERT INTO people_index (name) VALUES('{}')").format((name)))
    conn.commit()
    conn.close()

def insert_rating(game, person, rating):
    #not currently functional
    #insert a rating into the narrow rating table
    conn = psycopg2.connect('dbname = boardgames user = postgres')
    cur = conn.cursor()
    cur.execute(("SELECT COUNT('rating ID') FROM narrow_ratings WHERE game_id = (SELECT id FROM games WHERE name = '{}') AND person_id = (SELECT id FROM people_index WHERE name = '{}');").format(game, person))
    if cur.fetchall()[0]:
        update_rating(game, person, rating)
        conn.commit()
        conn.close()
        return None
    cur.execute(("INSERT INTO narrow_ratings (game_id, person_id, rating) VALUES ((SELECT id FROM games WHERE name = '{}'), (SELECT id FROM people_index WHERE name = '{}'), '{}'); ").format(game, person, rating))
    conn.commit()
    conn.close()

def insert_ratings(game, people, ratings):
    '''inserts a rating into the SQL database for each person listed
    inputs: string, list, list
    outputs = None
    '''
    conn = psycopg2.connect('dbname = boardgames user = postgres')
    for value in range(len(people)):
        cur = conn.cursor()
        cur.execute(("SELECT COUNT('rating_id') FROM narrow_ratings WHERE game_id = (SELECT id FROM games WHERE name = '{}') AND person_id = (SELECT id FROM people_index WHERE name = '{}');").format(game, people[value]))
        if cur.fetchall()[0][0]:
            update_rating(game, people[value], ratings[value])
            continue
        cur.execute(("INSERT INTO narrow_ratings (game_id, person_id, rating) VALUES ((SELECT id FROM games WHERE name = '{}'), (SELECT id FROM people_index WHERE name = '{}'), '{}'); ").format(game, people[value], ratings[value]))
        conn.commit()
    conn.close()

def update_rating(game, person, rating):
    '''updates a created rating
    inputs = string, string, float
    output = None
    '''
    conn = psycopg2.connect('dbname = boardgames user = postgres')
    cur = conn.cursor()
    cur.execute(('''UPDATE narrow_ratings SET rating = '{}' WHERE game_id = (SELECT id FROM games WHERE name = '{}') 
        AND person_id = (SELECT id FROM people_index WHERE name = '{}'); ''').format(rating, game, person))
    conn.commit()
    conn.close()

def all_ratings():
    '''Returns an object containing all ratings list ordered by user_id
    inputs = None
    outputs = table of person, ratings
    '''
    conn = psycopg2.connect('dbname = boardgames user = postgres')
    cur = conn.cursor()
    cur.execute('SELECT games.name AS game, people_index.name as Person, narrow_ratings.rating FROM games RIGHT JOIN narrow_ratings ON games.id = narrow_ratings.game_id LEFT JOIN people_index ON people_index.id = narrow_ratings.person_id');
    ratings = cur.fetchall()
    return ratings

def update_durations(games, lengths):
    '''A tool for updating the lengths of multiple board games at once.
    inputs = list of game names, list of durations
    outputs: None
    '''
    conn = psycopg2.connect('dbname = boardgames user = postgres')
    for index, name in enumerate(games):
        cur = conn.cursor()
        cur.execute(("UPDATE games SET duration = {} WHERE name = '{}'").format(lengths[index], name))
        conn.commit()
    conn.close()
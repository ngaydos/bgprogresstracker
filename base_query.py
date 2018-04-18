import psycopg2

conn = psycopg2.connect('dbname = boardgames user = postgres')
cur = conn.cursor()

cur.execute("SELECT COUNT(name) FROM games;")
game_count =  cur.fetchone()[0]

cur.execute("SELECT COUNT(name) FROM games WHERE played_2018 = True;")
played_count = cur.fetchone()[0]

print game_count
print played_count
import psycopg2

conn = psycopg2.connect('dbname = boardgames user = postgres')
cur = conn.cursor()

cur.execute("SELECT COUNT(name) FROM games;")
game_count =  cur.fetchone()[0]

cur.execute("SELECT COUNT(name) FROM games WHERE played_2018 = True;")
played_count = cur.fetchone()[0]

progress = float(played_count)/game_count

if __name__ == '__main__':
    print(round(progress, 3))
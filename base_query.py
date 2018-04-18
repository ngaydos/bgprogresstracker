import psycopg2

conn = psycopg2.connect('dbname = boardgames user = postgres')
cur = conn.cursor()


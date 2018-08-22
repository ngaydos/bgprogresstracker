from flask import render_template
from app import app
import psycopg2

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Nick'}
    posts = [
        {'author': {'username': 'Vadim'},
        'body': 'I sure hate seven wonders'
        }
    ]
    return render_template('index.html', title = 'Index', user = user)

@app.route('/collection')
def collection():
    conn = psycopg2.connect('dbname = boardgames user = postgres')
    cur = conn.cursor()
    cur.execute('SELECT * FROM games')
    games = [item[0] for item in cur.fetchall()]
    return render_template('collection.html', title = 'Collection', games = games)
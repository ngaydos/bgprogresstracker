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

@app.route('/game/<gamename>')
def game(gamename):
    conn = psycopg2.connect('dbname = boardgames user = postgres')
    cur = conn.cursor()
    cur.execute(("SELECT * FROM games WHERE name = '{}'").format(gamename))
    gameinfo = cur.fetchall()[0]
    name = gameinfo[0]
    min_players = gameinfo[1]
    max_players = gameinfo
    return render_template('game.html', name = gameinfo[0], 
        min_players = gameinfo[1], max_players = gameinfo[2], best_count = gameinfo[3],
         type = gameinfo[4], duration= gameinfo[5], played_2018 = gameinfo[6])
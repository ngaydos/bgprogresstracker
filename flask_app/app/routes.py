from flask import render_template, redirect, request, flash
from app.forms import GameForm, ReviewForm
from app import app
import psycopg2
from app.misc.sqlmod import insert_rating, update_rating

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

@app.route('/collection', methods = ['GET', 'POST'])
def collection():
    form = GameForm()
    if request.method == 'POST':
        return redirect('/game/{}'.format(form.game_select.data)) 
    elif request.method == 'GET':
        conn = psycopg2.connect('dbname = boardgames user = postgres')
        cur = conn.cursor()
        cur.execute('SELECT * FROM games')
        games = [item[0] for item in cur.fetchall()]

        return render_template('collection.html', title = 'Collection', games = games, form = form)

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

@app.route('/review', methods = ['GET', 'POST'])
def review():
    form = ReviewForm()
    if request.method == 'POST' and form.validate_on_submit():
        insert_rating(form.game.data, form.person.data, form.rating.data)
        flash(('Rating of {} inserted for game {} for {}').format(form.rating.data, form.game.data, form.rating.data))
    elif request.method == 'GET':
        return render_template('review.html', title = 'Game Rating Update' form = form)
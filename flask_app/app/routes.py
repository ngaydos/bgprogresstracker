from flask import render_template, redirect, request, flash
from app.forms import GameForm, ReviewForm, PlayerCountForm
from app import app
import psycopg2
from app.misc.sqlmod import insert_rating, update_rating

@app.route('/')
@app.route('/index')
def index():
    conn = psycopg2.connect('dbname = boardgames user = postgres')
    cur = conn.cursor()
    cur.execute("SELECT COUNT(name) FROM games;")
    game_count =  cur.fetchone()[0]
    cur.execute("SELECT COUNT(name) FROM games WHERE played_2018 = True;")
    played_count = cur.fetchone()[0]
    played_rate = float(played_count)/game_count
    return render_template('index.html', title = 'Home', game_count = game_count, played_count = played_count, played_rate = round(played_rate, 3 ))

@app.route('/collection', methods = ['GET', 'POST'])
def collection():
    gameform = GameForm()
    playerform = PlayerCountForm()
    if request.method == 'POST':
        if gameform.game_select.data != 'None':
            return redirect('/game/{}'.format(gameform.game_select.data))
        else:
            return redirect('/collection')
    elif request.method == 'GET':
        conn = psycopg2.connect('dbname = boardgames user = postgres')
        cur = conn.cursor()
        cur.execute('SELECT * FROM games')
        games = [item[0] for item in cur.fetchall()]

        return render_template('collection.html', title = 'Collection', games = games, gameform = gameform, playerform= playerform)

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
    if request.method == 'POST':
        insert_rating(form.game.data, form.person.data, form.rating.data)
        flash(('Rating of {} inserted for game {} for {}').format(form.rating.data, form.game.data, form.person.data))
        return redirect('review')
    elif request.method == 'GET':
        return render_template('review.html', title = 'Game Rating Update', form = form)
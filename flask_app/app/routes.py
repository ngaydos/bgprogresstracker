from flask import render_template, redirect, request, flash
from app.forms import GameForm, ReviewForm, PlayerCountForm, NewGameForm
from app import app
import psycopg2
from app.misc.sqlmod import insert_rating, update_rating
#general imports


@app.route('/')
@app.route('/index')
#defines index by both the base page and the index
def index():
    #connects to database to gain basic information for front page
    conn = psycopg2.connect('dbname = boardgames user = postgres')
    cur = conn.cursor()
    cur.execute("SELECT COUNT(name) FROM games;")
    game_count =  cur.fetchone()[0]
    cur.execute("SELECT COUNT(name) FROM games WHERE played_2018 = True;")
    played_count = cur.fetchone()[0]
    played_rate = float(played_count)/game_count
    return render_template('index.html', title = 'Home', game_count = game_count, played_count = played_count, played_rate = round(played_rate, 3 ))

@app.route('/collection', methods = ['GET', 'POST'])
#sets up collection page
def collection():
    #uses two independent forms depending on which form the user is submitting
    gameform = GameForm()
    playerform = PlayerCountForm()
    conn = psycopg2.connect('dbname = boardgames user = postgres')
    cur = conn.cursor()
    cur.execute('SELECT * FROM games')
    games = [item[0] for item in cur.fetchall()]
    if request.method == 'POST':
        if gameform.game_select.data != 'None':
            return redirect('/game/{}'.format(gameform.game_select.data))
        elif playerform.submit.data:
            if playerform.validate_on_submit():
                return search(playerform.player_count.data, playerform.must_be_new.data)
            else:
                return render_template('/collection.html', title = 'Collection', games = games, gameform = gameform, playerform = playerform)
        else:
            return render_template('collection.html', title = 'Collection', games = games, gameform = gameform, playerform= playerform)
    elif request.method == 'GET':
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

@app.route('/search')
def search(player_count, played_bool):
    conn = psycopg2.connect('dbname = boardgames user = postgres')
    cur = conn.cursor()
    if played_bool == 'y':
        cur.execute(("SELECT name FROM games WHERE played_2018 = 'False' AND min_players <={} AND max_players >= {}").format
            (player_count, player_count))
    else:
        cur.execute(("SELECT name FROM games WHERE min_players <={} AND max_players >= {}").format
            (player_count, player_count))
    gamelist = [item[0] for item in cur.fetchall()]
    return render_template('search.html', title = 'Search Results', gamelist = gamelist)

@app.route('/newgame', methods = ['GET', 'POST'])
def newgame():
    conn = psycopg2.connect('dbname = boardgames user = postgres')
    cur = conn.cursor()
    form = NewGameForm()
    if request.method == 'POST':
        cur.execute(("INSERT INTO games(name, min_players, max_players, duration, played_2018) VALUES({}, {}, {}, {}, {})").format
            (form.game_name.data, form.min_players.data, form.max_players.data, form.duration.data, form.played_2018.data))
        if form.best_count != 'None':
            cur.execute(("UPDATE games SET best_count = {} WHERE name = {}").format(form.best_count.data, form.game_name.data))
        if form.genre != 'None':
            cur.execute(("UPDATE games SET genre = {} WHERE name = {}").format(form.genre.data, form.game_name.data))
        conn.commit()
        conn.close()
    return render_template('newgame.html', title = 'New Game Information', form = form)
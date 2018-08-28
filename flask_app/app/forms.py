import psycopg2
from flask_wtf import FlaskForm
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField


class GameForm(FlaskForm):
    conn = psycopg2.connect('dbname = boardgames user = postgres')
    cur = conn.cursor()
    cur.execute('SELECT * FROM games ORDER BY name')
    games = [(item[0], item[0]) for item in cur.fetchall()]
    game_select = SelectField('Game Name', choices = games)
    submit =  SubmitField('Select')

class ReviewForm(FlaskForm):
    conn = psycopg2.connect('dbname = boardgames user = postgres')
    cur = conn.cursor()
    cur.execute('SELECT * FROM games ORDER BY name')
    games = [(item[0], item[0]) for item in cur.fetchall()]
    cur.execute('SELECT * FROM people_index ORDER BY name')
    people = [(item[0], item[0]) for item in cur.fetchall()]
    person = SelectField('Person', choices = people)
    game = SelectField('Game', choices = games)
    rating = IntegerField('Rating')
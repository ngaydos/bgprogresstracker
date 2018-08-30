import psycopg2
from flask_wtf import FlaskForm
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField, FloatField
from wtforms.validators import DataRequired


class GameForm(FlaskForm):
    conn = psycopg2.connect('dbname = boardgames user = postgres')
    cur = conn.cursor()
    cur.execute('SELECT * FROM games ORDER BY name')
    games = [(item[0], item[0]) for item in cur.fetchall()]
    game_select = SelectField('Game Name', choices =[(None, 'SELECT ONE')] + games)
    submit =  SubmitField('Select')

class ReviewForm(FlaskForm):
    conn = psycopg2.connect('dbname = boardgames user = postgres')
    cur = conn.cursor()
    cur.execute('SELECT * FROM games ORDER BY name')
    games = [(item[0], item[0]) for item in cur.fetchall()]
    cur.execute('SELECT * FROM people_index ORDER BY name')
    people = [(item[1], item[1]) for item in cur.fetchall()]
    person = SelectField('Person', choices = people)
    game = SelectField('Game', choices = games)
    rating = FloatField('Rating')
    submit = SubmitField('Submit')

class PlayerCountForm(FlaskForm):
    player_count = IntegerField('Player Count', validators = [DataRequired()])
    must_be_new = RadioField('Only Select Unplayed 2018?', choices = [('y', 'Yes'), ('n', 'No')], validators = [DataRequired()])
    submit = SubmitField('Search')
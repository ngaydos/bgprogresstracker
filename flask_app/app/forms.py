import psycopg2
from flask_wtf import FlaskForm
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField


class GameForm(FlaskForm):
    conn = psycopg2.connect('dbname = boardgames user = postgres')
    cur = conn.cursor()
    cur.execute('SELECT * FROM games')
    games = [(item[0], item[0]) for item in cur.fetchall()]
    game_select = SelectField('Game Name', choices = games)
    submit =  SubmitField('Select')
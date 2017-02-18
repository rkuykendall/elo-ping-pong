import datetime
import os
import sys
import logging

from flask import Flask, render_template, request, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy

from ranking import ranking

app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)


if 'DATABASE_URL' in os.environ:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    winner = db.Column(db.String(500))
    loser = db.Column(db.String(500))
    created_asof = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_asof = db.Column(
        db.DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow)

    def __init__(self, winner, loser):
        self.winner = winner
        self.loser = loser


db.create_all()


@app.route('/new', methods=['POST'])
def new():
    winner = request.form['winner']
    loser = request.form['loser']
    match = Match(winner, loser)
    db.session.add(match)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/')
def index():
    matches = db.session.query(Match).order_by(Match.created_asof.desc())
    rankings = ranking(matches)
    return render_template('index.html', matches=matches, rankings=rankings)


if __name__ == '__main__':
    app.run(debug=True)

import pymysql
import os
import monopoly
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy()
# create the app
app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")

# initialize the app with Flask-SQLAlchemy
db.init_app(app)

# each table in the database needs a class to be created for it
# this class is named Sock because the database contains info about socks
# and the table in the database is named: socks
# db.Model is required - don't change it
# identify all columns by name and their data type
class Roll(db.Model):
    __tablename__ = 'rolls'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    color = db.Column(db.String)
    roll_count = db.Column(db.Integer)


# NOTHING BELOW THIS LINE NEEDS TO CHANGE
# this route will test the database connection - and nothing more
@app.route('/')
def index():
    try:
        roll_table = db.session.execute(db.select(Roll)).scalars()

        return render_template('index.html', roll_table=roll_table)
    
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

#you have to do thing = monopoly.main(num) to run the script

@app.route('/submit', methods=['POST'])
def submit():
    try:
        num = request.form['rollnumber']
        #put the output of monopoly.main(num) in a python list
        listrolls = monopoly.main(num)
        return render_template('submit.html', listrolls=listrolls)
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text


if __name__ == '__main__':
    app.run(port=4999, debug=True)
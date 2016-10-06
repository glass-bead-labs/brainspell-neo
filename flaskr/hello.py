from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash
import os
import sqlite3
import pymysql

app = Flask(__name__)
app.config.from_object(__name__)

hostname = '192.168.99.100'
username = 'root'
password = 'beo8hkii'
database = 'brainspell'



# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'brainspell_sanitized.sql'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
myConnection = pymysql.connect(host = hostname, user = username, passwd = password, db = database)


# DATABASE CONNECTION;
def connect_db():  # Connecting with sqlite3 for now (Use pymysql)?
    rv = pymysql.connect(host = hostname, user = username, passwd = password, db = database)
    return rv


def get_db():
    if not hasattr(g, ''):
        g.sqlite_db = connect_db
    return g.sqlite_db()


# @app.teardown_appcontext
# def close_db(error):
#     """Closes the database again at the end of the request."""
#     if hasattr(g, 'sqlite_db'):
#         g.close()

def init_db():
    return connect_db().cursor()


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')




@app.route('/')
def show_main():
    #flash('This screen will show one article to test database connection')
    db = myConnection.cursor()
    db.execute('Select UniqueID from Articles WHERE UniqueID = 3290')
    for item in db.fetchall():
        return item






# return render_template('hello.html', name=name) Renders hello.html


@app.route('/go')
def search():
    return render_template("text.html")


@app.route('/data', methods=['GET', 'POST'])
def post():
    return "hi"


if __name__ == "__main__":
    app.debug = True
    app.run()

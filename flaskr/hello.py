#Installs
#pip install requests-aws4auth


#String of imports. Delete what's not useful later
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, jsonify
import os
import sqlite3
import pymysql # will be using this as a search engine for the time being
import sqlalchemy as sql

from elasticsearch import Elasticsearch
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import certifi




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


host = 'brainspell-postgres.camtj8eoxvnf.us-west-2.rds.amazonaws.com'
awsauth = AWS4Auth('AKIAI3X2XHIGRI3QGY4Q', 'eAbExEw0MTS/2HuC+5vyvWJc3aY+xoNMj9rv35hm', 'us-west-2', 'es')

es = Elasticsearch(
    hosts = [{'host': host, 'port': 5432}],
    http_auth = awsauth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection
)


@app.route('/database')
def database():
    return es.info()


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
    return 'Nothing'
    #flash('This screen will show one article to test database connection')
    # db = myConnection.cursor()
    # db.execute('Select UniqueID from Articles WHERE UniqueID = 3290')
    # for item in db.fetchall():
    #     return item







@app.route('/go')
def search():
    return render_template("text.html")


@app.route('/data', methods=['GET', 'POST'])
def post():
    text = request.form['text']
    cur = myConnection.cursor()
    search_term = '% ' + text + '%'
    search_string = "Select UniqueID,TIMESTAMP,Title,Authors,Abstract,Reference, PMID, DOI, NeuroSynthID, Experiments, Metadata from Articles WHERE Experiments LIKE '% hi%'"
    cur.execute(search_string)
    for UniqueID,TIMESTAMP,Title,Authors,Abstract,Reference,PMID,DOI,NeuroSynthID,Experiments,Metadata in cur.fetchall():
        database_dict = {}
        database_dict["UniqueID"] = UniqueID
        database_dict["TIMESTAMP"] = TIMESTAMP
        database_dict["Title"] = Title
        database_dict["Authors"] = Authors
        database_dict["Abstract"] = Abstract
        database_dict["Reference"] = Reference
        database_dict["PMID"] = PMID
        database_dict["DOI"] = DOI
        database_dict["NeuroSynthID"] = NeuroSynthID
        database_dict["Experiments"] = Experiments
        database_dict["Metadata"] = Metadata
    return jsonify(database_dict)



if __name__ == "__main__":
    app.debug = True
    app.run()

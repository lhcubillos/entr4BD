import os
import sys
import psycopg2
import pymongo

from pymongo import MongoClient
# from flask_bootstrap import Bootstrap
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

# reload(sys)
# sys.setdefaultencoding('utf-8')

def create_app():
  app = Flask(__name__)
  # Bootstrap(app)
  return app

app = create_app()

# Mongo config
MONGODATABASE = "myDatabase"
# MONGOCOLLECTION = "myCollection"
MONGOSERVER = "localhost"
MONGOPORT = 27017
client = MongoClient(MONGOSERVER, MONGOPORT)
mongodb = client[MONGODATABASE]

# Postgres config
POSTGRESDATABASE = "mydatabase"
POSTGRESUSER = "myuser"
POSTGRESPASS = "mypass"
postgresdb = psycopg2.connect(database=POSTGRESDATABASE, user=POSTGRESUSER, password=POSTGRESPASS)


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        query = request.form['query']
        db = request.form['db']
        if db == 'postgres':
            return postgres(query)
        else:
            return mongo(query)
    else:
        return render_template('form.html')

@app.route("/file")
def file ():
    f = open('queries', 'r')
    database = "postgres"
    pairs = []
    for line in f:
        line = line[:-1]
        if not line or line[0] == '#':
            continue
        elif line[0:2] == '//':
            database = line[3:]
        else:
            pairs.append([database, line, eval('{}(line)'.format(database))])
    return render_template('file.html', results = pairs)

@app.route("/mongo")
def mongo(query):
    return list(eval('mongodb.{}'.format(query)))

@app.route("/postgres")
def postgres(query):
    cursor = postgresdb.cursor()
    cursor.execute(query)
    return [list(result) for result in cursor]

if __name__ == "__main__":
    app.debug = True
    app.run()

import os
import sys
import psycopg2
import pymongo

from pymongo import MongoClient
# from flask_bootstrap import Bootstrap
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

reload(sys)
sys.setdefaultencoding('utf-8')

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


# @app.route("/", methods=['GET', 'POST'])
# def home():
#     if request.method == 'POST':
#         query = request.form['query']
#         db = request.form['db']
#         if db == 'postgres':
#             return postgres(query)
#         else:
#             return mongo(query)
#     else:
#         return render_template('form.html')

@app.route("/")
def home ():
    f = open('queries', 'r')
    database = "postgres"
    pairs = []
    for line in f:
        line = line.rstrip()
        if not line or line[0] == '#':
            continue
        elif line[:2] == '//':
            database = line[3:]
        else:
            # pairs.append([database, line, eval('{}(line)'.format(database))])
            pairs.append([database, line])
    return render_template('file.html', results = enumerate(pairs))

@app.route("/mongo/<query>")
def mongo(query):
    results = eval('mongodb.{}'.format(query))
    if "find" in query:
        return render_template('mongo.html', results=list(results))
    else:
        return "ok"


@app.route("/postgres/<query>")
def postgres(query):
    cursor = postgresdb.cursor()
    cursor.execute(query)
    results = [[a for a in result] for result in cursor]
    print (results)
    return render_template('postgres.html', results=results)

@app.route("/example")
def example():
    return render_template('example.html')

if __name__ == "__main__":
    app.debug = True
    app.run()

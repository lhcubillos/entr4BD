import os
import sys
import psycopg2
import pymongo
import json
from bson import json_util

from pymongo import MongoClient
# from flask_bootstrap import Bootstrap
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

reload(sys)
sys.setdefaultencoding('utf-8')

def create_app():
  app = Flask(__name__)
  return app

app = create_app()


QUERIES_FILENAME = 'queries'

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

@app.route("/")
def home():
    with open(QUERIES_FILENAME, 'r') as queries_file:
        json_file = json.load(queries_file)
        pairs = [(x["name"], x["database"], x["description"], x["query"]) for x in json_file]
        return render_template('file.html', results = pairs)

@app.route("/mongo")
def mongo():
    query = request.args.get("query")
    results = eval('mongodb.'+query)
    results = json_util.dumps(results, sort_keys=True, indent=4)
    if "find" in query:
        return render_template('mongo.html', results=results)
    else:
        return "ok"

@app.route("/postgres")
def postgres():
    query = request.args.get("query")
    cursor = postgresdb.cursor()
    cursor.execute(query)
    results = [[a for a in result] for result in cursor]
    print (results)
    return render_template('postgres.html', results=results)

if __name__ == "__main__":
    app.debug = True
    app.run()

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
    with open('queries', 'r') as queries_file:
        json_file = json.load(queries_file)
        pairs = [[x["name"], "postgres", x["description"], x["query"]] for x in json_file["postgres"]]
        pairs.extend([[x["name"], "mongo", x["description"], x["query"]] for x in json_file["mongo"]])
        return render_template('file.html', results = enumerate(pairs))

@app.route("/mongo")
def mongo():
    query = request.args.get("query")
    results = eval('mongodb.'+query)
    # results = json.dumps(results, sort_keys=True, indent=4, default=json_util.default)
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

@app.route("/example")
def example():
    return render_template('example.html')

if __name__ == "__main__":
    app.debug = True
    app.run()

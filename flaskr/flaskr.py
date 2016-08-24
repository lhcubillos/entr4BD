import os
import sys
import psycopg2
import pymongo

from pymongo import MongoClient
from flask_bootstrap import Bootstrap
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

reload(sys)
sys.setdefaultencoding('utf-8')

def create_app():
  app = Flask(__name__)
  Bootstrap(app)

  return app

app = create_app()

# Mongo config
MONGODATABASE = "myDatabase"
MONGOCOLLECTION = "myCollection"
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
def queries ():
    f = open('queries', 'r')
    database = "postgres"
    pairs = []
    for line in f:
        line = line.rstrip('\n')
        if (line[0:1] == '#'):
            database = line[2:]
        elif (len(line)>2):
            print (line)
            if (database == "postgres"):
                pairs.append([line, postgres(line)])
            else:
                pairs.append([line, mongo(line)])
    return render_template('file.html', results = pairs)

@app.route("/mongo")
def mongo(query):
    # cursor = mongodb[MONGOCOLLECTION].find()
    # myCollection.find()
    cursor = []
    if "find" in query:
        exec ("cursor = mongodb."+query)
        docs = []
        for doc in cursor:
            docs.append(doc)
        return str(docs)
    else:
        # myCollection.insert({'name': 'U2'})
        exec ("mongodb."+query)
        return "ok"

@app.route("/postgres")
def postgres(query):
    cursor = postgresdb.cursor()
    # cursor.execute("SELECT * FROM mytable;")
    cursor.execute("SELECT column_name, data_type, character_maximum_length FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name ='mytable'")
    schema = []
    for result in cursor:
        schema.append([element for element in result])

    cursor.execute(query)
    results = []
    for result in cursor:
        results.append([element for element in result])
    # return render_template('postgres.html', schema=schema, results=results)
    return results

if __name__ == "__main__":
    app.debug = True
    app.run()

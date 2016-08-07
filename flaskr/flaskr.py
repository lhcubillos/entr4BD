import os
import sys
import psycopg2
import pymongo
from pymongo import MongoClient
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash


app = Flask(__name__)


MONGODATABASE = "myDatabase"
MONGOCOLLECTION = "myCollection"
MONGOSERVER = "localhost"
MONGOPORT = 27017
client = MongoClient(MONGOSERVER, MONGOPORT)
mongodb = client[MONGODATABASE]

POSTGREDATABASE = "mydatabase"
POSTGREUSER = "myuser"
POSTGREPASS = "myPass"
postgredb = psycopg2.connect(database=POSTGREDATABASE, user=POSTGREUSER, password=POSTGREPASS)


@app.route("/")
def home():
    return "Hello World!"

@app.route("/mongo")
def mongo():
    cursor = mongodb[MONGOCOLLECTION].find()
    docs = []
    for doc in cursor:
    	docs.append(doc)

    return str(docs)


@app.route("/postgre")
def postgre():
    cursor = postgredb.cursor()
    cursor.execute("SELECT * FROM mytable;")

    return str(cursor.fetchall())

if __name__ == "__main__":
    app.run()

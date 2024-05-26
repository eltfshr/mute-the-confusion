from queue import Queue
import sqlite3
from flask import g

connection_pool = Queue(maxsize=1)


def get_db():
  if connection_pool.qsize() == 0:
    con = sqlite3.connect("mute_the_confusion.db", isolation_level=None, check_same_thread=False)
    con.execute("CREATE TABLE IF NOT EXISTS messages (message TEXT, owner TEXT);")
    connection_pool.put(con)
    g.db = con

  return connection_pool.get()


def close_db():
  db = g.pop('db', None)
  if db is not None:
    connection_pool.put(db)


def insert(message, owner):
  curr = get_db().cursor()
  curr.execute("INSERT INTO messages VALUES(?, ?)", (message, owner))


def get_messages():
  curr = get_db().cursor()
  curr.execute("SELECT * FROM messages ORDER BY ROWID DESC LIMIT 10;")
  results = curr.fetchall()

  response = []
  for result in results:
    response.insert(0, {
      "message": result[0],
      "owner": result[1]
    })
  return response


def get_all_messages():
  curr = get_db().cursor()
  curr.execute("SELECT * FROM messages ORDER BY ROWID DESC;")
  results = curr.fetchall()

  response = []
  for result in results:
    response.insert(0, {
      "message": result[0],
      "owner": result[1]
    })
  return response
from flask import Flask, jsonify, render_template, request
import json
import serial_comm
import db
import socketio
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)


@app.get("/")
def get_index():
  return render_template("index.html")


@app.get("/screen")
def get_screen():
  return render_template("screen.html")


@app.get("/all")
def get_all():
  return render_template("all.html")


@socketio.on('connect')
def connect():
  print('connect')


@app.get("/messages")
def get_messages():
  messages = db.get_messages()
  return jsonify({
    "messages": messages
  })


@app.get("/all_messages")
def get_all_messages():
  messages = db.get_all_messages()
  return jsonify({
    "messages": messages
  })


@app.post("/")
def post():
  message = request.form["message"]
  owner = request.form["from"]
  socketio.emit("message", {'message': message, 'owner': owner})
  db.insert(message, owner)
  return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


@app.teardown_request
def teardown_db(f):
  if request.endpoint == 'post':
    db.close_db()


@app.post("/buttons/<id>")
def post_buttons(id):
  serial_comm.write(id)
  return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


if __name__ == '__main__':
  socketio.run(app)
from flask import Flask, render_template, request
import json
import serial_comm

app = Flask(__name__)

@app.get("/")
def get_index():
  return render_template("index.html")

@app.post("/")
def post():
  print(request.form["message"])
  return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.post("/buttons/<id>")
def post_buttons(id):
  serial_comm.write(id)
  return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
import os
import requests
import time
from collections import deque

from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
from flask_socketio import SocketIO, send, emit, join_room, leave_room


app = Flask(__name__)
app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

users = []
channels = []
messages = {}


@app.route('/')
def index():
    if session.get('channel') is None:
        return render_template('index.html')

    return redirect(url_for('channel', channel_name=session['channel']))


@app.route('/main', methods=['GET', 'POST'])
def main():

    if request.method == 'POST':
        username = request.form.get('username')
        if len(username) == 0:
            return render_template('index.html', error="Username cannot be blank")

        if username in users:
            return render_template('index.html', error="User already exist")

        users.append(username)
        session['user'] = username
        session.permanent = True
        return render_template('main.html', channels=channels)

    if request.method == 'GET':
        if session.get('user') is None:
            return render_template('index.html', error="Provide username first")

        return render_template('main.html', channels=channels)


@app.route('/channel/<channel_name>')
def channel(channel_name):
    session['channel'] = channel_name
    return render_template('channel.html', channel_name=channel_name, messages=messages[channel_name])


@socketio.on('create channel')
def vote(data):
    channel_name = str(data["channel_name"])
    if channel_name in channels:
        yes = 0
        message = "Channel already exist"
        emit("announce channel", {"channel_name": channel_name,
                                  "message": message, "yes": yes}, broadcast=False)

    if channel_name not in channels:
        channels.append(channel_name)

        # every channel has a queue associated with it
        messages[channel_name] = deque()
        message = "Channel Created Successfully"
        yes = 1
        emit("announce channel", {"channel_name": channel_name,
                                  "message": message, "yes": yes}, broadcast=True)
        yes = 0
        emit("announce channel", {"channel_name": channel_name,
                                  "message": message, "yes": yes}, broadcast=False)


@socketio.on("joined")
def joined():
    room = session.get('channel')
    user = session.get('user')

    emit("status", {"username": user, "room": room,
                    "msg": user + ' has joined the channel!'}, broadcast=True)


@socketio.on("leaved")
def leaved():
    room = session.get('channel')
    user = session.get('user')

    emit("status_leave", {"username": user, "room": room,
                          "msg": user + ' has leaved the channel!'}, broadcast=True)


@socketio.on("comment")
def comment(data):
    room = session.get('channel')

    if len(messages[room]) > 100:
        messages[room].popleft()

    username = session.get('user')
    comment = data["comment"]
    interval = time.strftime(' %B, %d %H:%M')

    # every message having username and time associated with it
    messages[room].append([username, comment, interval])
    emit("message", {"username": username,
                     "comment": comment, "interval": interval}, broadcast=True)

import os

from flask import Flask, session, render_template, request, jsonify, redirect, url_for
from flask_session import Session
from flask_socketio import SocketIO, emit, rooms
from channel import Channel

app = Flask(__name__)


app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Keep track of chat channels
channels = {}


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        if 'username' not in session:
            return render_template("start_here.html")

        return render_template("channels.html", channels=channels)
    if request.method == "POST":
        username = request.form.get("username")
        if username is None:
            return render_template("error.html", message="choose a username")
        session['username'] = username
        return redirect(url_for('index'))

@app.route("/create_channel", methods=["POST"])
def create():


    # Make sure the name valid, i.e. not taken, not empty
    if name is None:
        return jsonify({"success": False})
    if name in channels.keys():
        return jsonify({"success": False})

    # Create the new channel
    channel = Channel(name=name)
    channels[name] = channel

    print(channels)

    return jsonify({"success": True})

@socketio.on("create channel")
def createChannel(data):

    # Get the channel name
    name = data['name']

    # Make sure the name valid, i.e. not taken, not empty
    if name is None:
        emit("channel created", {"success": False})
    if name in channels.keys():
        emit("channel created", {"success": False})

    # Create the new channel
    channel = Channel(name=name)
    channels[name] = channel

    # Broadcast new channel to users
    emit("channel created", {"success": True}, broadcast=True)


@app.route("/channel/<string:channelName>")
def channel(channelName):
    print(session["username"])

    # Make sure the channel exists
    if channelName not in channels.keys():
        return render_template("error.html", message="no such channel")
    channel = channels[channelName]

    # Keep track of user joining the channel
    session["channel"] = channelName

    return render_template("chat.html", channel=channel)

@socketio.on("send message")
def message(data):

    # Get the message
    message = data["message"]

    # Save message in channel history
    channel = channels[session["channel"]]
    channel.addMessage(message)

    emit("new message", {"message": message}, broadcast=True)

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
channels = []


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
    print([channel.name for channel in channels])

    # Get the new channel name
    name = request.form.get("name")

    # Make sure the name is not empty and isn't already taken
    if name is None:
        return jsonify({"success": False})
    if name in [channel.name for channel in channels]:
        return jsonify({"success": False})

    # Create the new channel
    channel = Channel(name=name)
    channels.append(channel)

    print(channels)

    return jsonify({"success": True})

@app.route("/channel/<string:channelName>")
def channel(channelName):

    # Make sure the channel exists
    if channelName not in [channel.name for channel in channels]:
        return render_template("error.html", message="no such channel")


    return render_template("chat.html", channel=channels[channelName])

@socketio.on("send message")
def message(data):
    # room = data["channel"]
    message = data["message"]
    emit("new message", {"message": message}, broadcast=True)

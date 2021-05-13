import chess
import chess.svg
import os
from flask import Flask, send_from_directory, json, request
from flask_socketio import SocketIO, join_room, leave_room
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv(find_dotenv())

APP = Flask(__name__, static_folder='../build/static')

# APP.config['SQLALCHEMY_DATABASE_URI'] = "os.getenv('DATABASE_URL')"
# APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# DB = SQLAlchemy(APP)

# import models  # pylint: disable=wrong-import-position

CORS = CORS(APP, resources={r"/*": {"origins": "*"}})

SOCKETIO = SocketIO(APP,
                    cors_allowed_origins="*",
                    json=json,
                    manage_session=False)

board = chess.Board()

@APP.route('/', defaults={"filename": "index.html"})
@APP.route('/<path:filename>')
def index(filename):
    '''Tells python where our index file is that renders our React Components'''
    return send_from_directory('../build', filename)

# When a client connects from this Socket connection, this function is run
@SOCKETIO.on('connect')
def on_connect():
    '''When someone connects to the server'''
    print('User connected!')

# When a client disconnects from this Socket connection, this function is run
@SOCKETIO.on('disconnect')
def on_disconnect():
    '''When a player disconnects from the server, we get their name
    from their session id and remove them from the lobby'''
    print('User Disconnected')

@SOCKETIO.on('fetchboard')
def fetchboard():
    passBoard = str(board.fen())
    print(passBoard)
    SOCKETIO.emit('fetchboard', {'board': passBoard})

@SOCKETIO.on('move')
def move(data):
    moveTo = data['moveTo']
    print(moveTo)
    piece = chess.Move.from_uci(moveTo)
    board.push(piece)
    print(board)
    SOCKETIO.emit('fetchboard', {'board': str(board.fen())})

if __name__ == "__main__":
    # DB.create_all()
    # pylint: disable=invalid-envvar-default
    SOCKETIO.run(
        APP,
        debug=True,
        host='localhost',
        port=5000)
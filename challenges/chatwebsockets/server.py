from flask import Flask, send_from_directory, request, jsonify
from flask_socketio import SocketIO, send
import requests
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

messages = []

def fetch_random_users():
    response = requests.get('https://randomuser.me/api/?results=10')
    return response.json()['results']

def fetch_random_images():
    response = requests.get('https://picsum.photos/v2/list?page=2&limit=100')
    return response.json()

random_users = fetch_random_users()
random_images = fetch_random_images()

print(random_users)
print(random_images)

@app.route('/')
def index():
    return send_from_directory(os.getcwd(), 'index.html')

@app.route('/api/users')
def get_users():
    return jsonify(random_users)

@app.route('/api/images')
def get_images():
    return jsonify(random_images)

@socketio.on('message')
def handle_message(msg):
    print(f"Received: {msg}")
    messages.append(msg)  # Store the message
    send(msg, broadcast=True)  # Broadcast the message to all clients

if __name__ == '__main__':
    socketio.run(app, debug=True)
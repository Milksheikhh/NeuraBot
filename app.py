from flask import Flask, render_template, jsonify
from bot_movement import move_to_room
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check_status/<room>')
def check_status(room):
    try:
        with open('bot_status.txt', 'r') as f:
            text = f.read().strip().split()
            status = text[0]
            currentroom = text[1]
            if currentroom == room:
                return jsonify({'status': 'at room', 'currentroom': currentroom})
            if status == "ready":
                threading.Thread(target=move_to_room, args=(room, currentroom)).start()
        return jsonify({'status': status, 'current_room': currentroom})
    except Exception as e:
        return jsonify({'status': 'error'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2000)
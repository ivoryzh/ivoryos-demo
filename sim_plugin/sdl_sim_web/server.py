from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

last_known_state = {"vial_location": "tray", "is_held_by_arm": False}

@socketio.on('connect')
def handle_connect():
    socketio.emit('sync_state', last_known_state)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/event', methods=['POST'])
def handle_event():
    global last_known_state
    data = request.json
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
        
    print(f"Received event: {data}")
    
    if data.get('instrument') == 'system' and data.get('action') == 'sync_state':
        if data.get('args') and len(data['args']) > 0:
            last_known_state = data['args'][0]
        socketio.emit('sync_state', last_known_state)
    else:
        # Broadcast event to all connected clients
        socketio.emit('instrument_event', data)
        
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    # Run the server on port 5000
    socketio.run(app, debug=True, port=5000)

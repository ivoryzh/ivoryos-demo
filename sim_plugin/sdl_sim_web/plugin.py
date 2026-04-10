from flask import Blueprint, render_template, request, jsonify
from flask_socketio import emit

web_viz_bp = Blueprint('web_viz', __name__, template_folder='templates', static_folder='static')
web_viz_bp.plugin_type = "left_panel"
web_viz_bp.last_known_state = {"vial_location": "tray", "is_held_by_arm": False}

_socketio = None

def init_socketio(socketio):
    global _socketio
    _socketio = socketio

    @_socketio.on('request_sync_state')
    def handle_request_sync_state():
        print("Client requested sync_state, emitting state: ", web_viz_bp.last_known_state)
        emit('sync_state', web_viz_bp.last_known_state)

web_viz_bp.init_socketio = init_socketio

@web_viz_bp.route('/')
def main():
    # If the user accesses the plugin main page directly via the url
    return render_template('web_viz.html')

@web_viz_bp.route('/widget')
def widget():
    return render_template('web_viz.html')

def process_event(data):
    if data.get('instrument') == 'system' and data.get('action') == 'sync_state':
        if data.get('args') and len(data['args']) > 0:
            web_viz_bp.last_known_state = data['args'][0]
        if _socketio:
            _socketio.emit('sync_state', web_viz_bp.last_known_state)
    else:
        # Broadcast event to all connected clients
        if _socketio:
            _socketio.emit('instrument_event', data)

@web_viz_bp.route('/event', methods=['POST'])
def handle_event():
    data = request.json
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
        
    process_event(data)
        
    return jsonify({"status": "ok"}), 200

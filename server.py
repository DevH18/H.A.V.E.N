from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Current state of HAVEN
current_state = {"state": "idle"}

@app.route('/state', methods=['GET'])
def get_state():
    return jsonify(current_state)

@app.route('/set/<new_state>', methods=['POST'])
def set_state(new_state):
    current_state["state"] = new_state
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(port=5000)
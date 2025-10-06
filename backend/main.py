from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)

# 👇 Enable CORS for every domain (broadest, easiest test)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/", methods=["POST"])
def simulate():
    data = request.get_json() or {}
    print("Received data:", data)

    # --- placeholder so we can test frontend <-> backend connection ---
    frames = [
        [[0, 0], [0, 1], [1, 1]],
        [[1, 2], [2, 2], [2, 3]]
    ]

    return jsonify({"frames": frames})


@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "Backend is alive and CORS open!"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # 👇 host must be 0.0.0.0 for Render to detect the port
    app.run(host="0.0.0.0", port=port, debug=False)

# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from train_and_run import run_simulation

app = Flask(__name__)
CORS(app)  # allow access from your GitHub Pages site

@app.route("/simulate", methods=["POST"])
def simulate():
    data = request.get_json()
    algo = data.get("algorithm", "q_learning")
    grid_size = tuple(data.get("grid_size", [4, 5]))
    num_obs = int(data.get("num_obstacles", 3))
    frames = run_simulation(algo, grid_size, num_obs, episodes=200)
    return jsonify({"frames": frames})

if __name__ == "__main__":
    app.run(debug=True)

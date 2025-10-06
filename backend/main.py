from flask import Flask, request, jsonify
from flask_cors import CORS
from train_and_run import run_simulation

# Create Flask app
app = Flask(__name__)

# Allow requests from your GitHub Pages domain
CORS(app, origins=["https://yukkta-seelam.github.io"])

@app.route("/", methods=["POST"])
def simulate():
    try:
        data = request.get_json()
        algorithm = data.get("algorithm", "q_learning")
        grid_rows = int(data.get("rows", 4))
        grid_cols = int(data.get("cols", 5))
        num_obstacles = int(data.get("obstacles", 2))
        episodes = int(data.get("episodes", 50))

        # Run simulation
        frames = run_simulation(algorithm, (grid_rows, grid_cols), num_obstacles, episodes)

        # Return as JSON response
        return jsonify({"frames": frames})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "Backend is alive!"})


if __name__ == "__main__":
    # Bind to 0.0.0.0 for Render and set PORT env var
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

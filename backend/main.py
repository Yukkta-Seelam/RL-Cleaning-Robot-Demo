from flask import Flask, request, jsonify, make_response
import os

app = Flask(__name__)

# ✅ Manually add CORS headers to every response (Render-safe)
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "https://yukkta-seelam.github.io"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response


@app.route("/", methods=["POST", "OPTIONS"])
def simulate():
    if request.method == "OPTIONS":
        # Preflight request — send empty response with headers
        return make_response("", 200)

    try:
        data = request.get_json() or {}
        print("✅ Received from frontend:", data)

        # Temporary placeholder to confirm connection
        frames = [
            [[0, 0], [0, 1], [1, 1]],
            [[1, 2], [2, 2], [2, 3]]
        ]
        return jsonify({"frames": frames})

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "Backend is alive and CORS manually set"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

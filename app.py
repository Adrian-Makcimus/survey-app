import os
import pandas as pd
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# CSV file to save responses
CSV_FILE = "responses.csv"

# Initialize CSV file with headers if it doesn't exist
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=["timestamp", "ip", "user_agent", "data"])
    df.to_csv(CSV_FILE, index=False)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json  # jsPsych data
    if data is None:
        return jsonify({"status": "error", "message": "No data received"}), 400

    record = {
        "timestamp": pd.Timestamp.utcnow(),
        "ip": request.headers.get("X-Forwarded-For", request.remote_addr),
        "user_agent": request.headers.get("User-Agent"),
        "data": str(data)  # store as stringified JSON
    }

    # Append to CSV
    df = pd.DataFrame([record])
    df.to_csv(CSV_FILE, mode="a", header=False, index=False)

    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

from flask import Flask, render_template, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

CSV_FILE = "responses.csv"
if not os.path.exists(CSV_FILE):
    pd.DataFrame(columns=["timestamp", "ip", "user_agent", "data"]).to_csv(CSV_FILE, index=False)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    if data:
        df = pd.DataFrame([{
            "timestamp": pd.Timestamp.utcnow(),
            "ip": request.headers.get("X-Forwarded-For", request.remote_addr),
            "user_agent": request.headers.get("User-Agent"),
            "data": str(data)
        }])
        df.to_csv(CSV_FILE, mode="a", header=False, index=False)
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)

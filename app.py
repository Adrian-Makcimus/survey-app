import os, json, datetime
from flask import Flask, request, jsonify, render_template
from psycopg2 import connect
from psycopg2.extras import Json

app = Flask(__name__)

DB_URL = os.getenv("DATABASE_URL")  # Set automatically if you add Render Postgres

def ensure_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS responses (
              id SERIAL PRIMARY KEY,
              submitted_at TIMESTAMPTZ DEFAULT NOW(),
              ip TEXT,
              user_agent TEXT,
              payload JSONB
            );
        """)
        conn.commit()

conn = None
if DB_URL:
    conn = connect(DB_URL, sslmode="require")
    ensure_table(conn)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/save", methods=["POST"])
def save():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"ok": False, "error": "No JSON received"}), 400

    record = {
        "ts": datetime.datetime.utcnow().isoformat() + "Z",
        "ip": request.headers.get("X-Forwarded-For", request.remote_addr),
        "ua": request.headers.get("User-Agent"),
        "data": data,
    }

    # Prefer Postgres if available; else append to a local JSONL file (good for quick testing)
    if conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO responses (ip, user_agent, payload) VALUES (%s, %s, %s)",
                (record["ip"], record["ua"], Json(record["data"]))
            )
            conn.commit()
    else:
        with open("responses.jsonl", "a") as f:
            f.write(json.dumps(record) + "\n")

    return jsonify({"ok": True})

@app.route("/done")
def done():
    return "<h2>Thanks! Your response was recorded.</h2>"

@app.get("/healthz")
def healthz():
    return "ok", 200

if __name__ == "__main__":
    # Local dev only
    app.run(host="0.0.0.0", port=8080, debug=True)

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Serve survey page
@app.route("/")
def index():
    return render_template("index.html")

# Collect survey results
@app.route("/submit", methods=["POST"])
def submit():
    data = request.json  # jsPsych data
    print("Received response:", data)  # (for debugging)
    # TODO: save to file or database
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

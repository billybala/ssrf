from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/admin/secret")
def secret():
    return jsonify({
        "secret": "FLAG(ssrf_internal_access_ok)",
        "message": "Este endpoint deberia ser inaccesible desde el exterior."
    })

@app.get("/")
def home():
    return "Internal service up"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

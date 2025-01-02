from flask import Flask, render_template, make_response
import os
import requests
import ast

app = Flask(__name__)

@app.route("/", strict_slashes=False)
def index():
    # Backend API details
    api_host = os.getenv("API_SERVER", "localhost")
    api_port = os.getenv("API_SERVER_PORT", "8080")

    try:
        # Fetch data from the backend
        response = requests.get(f"http://{api_host}:{api_port}/get_db_details")
        response.raise_for_status()
        response_data = response.json()

        # Extract cache status and data
        cache_hit = response_data.get("cache_hit", False)
        raw_data = response_data.get("data", "[]")

        # Parse the raw string data into a list of tuples
        db_data = ast.literal_eval(raw_data)

    except Exception as e:
        return render_template("error.html", error=str(e))

    return render_template("index.html", db_data=db_data, cache_hit=cache_hit)

@app.route("/status", strict_slashes=False)
def check_status():
    return make_response("OK", 200)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("APP_PORT", "8080")), debug=True)


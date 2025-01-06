from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
import redis
import os
from dotenv import load_dotenv
from flask_cors import CORS

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for the frontend to make requests

# MySQL Configuration
app.config['MYSQL_HOST'] = os.getenv('DB_HOST')
app.config['MYSQL_USER'] = os.getenv('DB_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('DB_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('DB_NAME')

# Redis Configuration
redis_host = os.getenv('REDIS_HOST')
redis_port = os.getenv('REDIS_PORT')

# Initialize MySQL and Redis
mysql = MySQL(app)
redis_cache = redis.StrictRedis(host=redis_host, port=int(redis_port), db=0)

@app.route('/<tablename>/get_db_details', methods=['GET'])
def get_db_details(tablename):
    try:
        # Validate the table name to prevent SQL injection
        if not tablename.isidentifier():
            return jsonify({"error": f"Invalid table name: {tablename}"}), 400

        # Check Redis cache for the table
        cache_key = f"db_details:{tablename}"
        cached_data = redis_cache.get(cache_key)
        if cached_data:
            return jsonify({
                "source": "cache",
                "cache_hit": True,
                "data": cached_data.decode('utf-8')
            })

        # Query the database
        cursor = mysql.connection.cursor()
        query = f"SELECT * FROM {tablename}"
        try:
            cursor.execute(query)
        except Exception as e:
            return jsonify({"error": f"No such table: {tablename}"}), 404

        db_data = cursor.fetchall()
        cursor.close()

        if db_data:
            db_details = str(db_data)
            redis_cache.setex(cache_key, 60, db_details)  # Cache data for 60 seconds

            return jsonify({
                "source": "database",
                "cache_hit": False,
                "data": db_details
            })
        else:
            return jsonify({
                "message": "No data found in the table"
            }), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/status', methods=['GET'])
def check_status():
    return jsonify({"status": "OK"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


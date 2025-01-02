from flask import Flask, jsonify
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

@app.route('/get_db_details', methods=['GET'])
def get_db_details():
    try:
        cached_data = redis_cache.get('db_details')

        if cached_data:
            return jsonify({
                "source": "cache",
                "cache_hit": True,
                "data": cached_data.decode('utf-8')
            })

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM sample_table")
        db_data = cursor.fetchall()
        cursor.close()

        if db_data:
            db_details = str(db_data)
            redis_cache.setex('db_details', 60, db_details)

            return jsonify({
                "source": "database",
                "cache_hit": False,
                "data": db_details
            })
        else:
            return jsonify({
                "message": "No data found in DB"
            }), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/status', methods=['GET'])
def check_status():
    return jsonify({"status": "OK"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


from flask import Flask, request, jsonify
import bcrypt
import requests
import pymysql
import os

JWT_SERVER = os.getenv('JWT_SERVER')
assert JWT_SERVER, "JWT_SERVER is not set"

# Load MySQL configuration from environment variables
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DB = os.getenv('MYSQL_DB')
MYSQL_PORT = os.getenv('MYSQL_PORT')

# Ensure that environment variables are set
assert MYSQL_HOST, "MYSQL_HOST is not set"
assert MYSQL_USER, "MYSQL_USER is not set"
assert MYSQL_PASSWORD, "MYSQL_PASSWORD is not set"
assert MYSQL_DB, "MYSQL_DB is not set"
assert MYSQL_PORT, "MYSQL_PORT is not set"


# Connect to MySQL database
try:
    db = pymysql.connect(
        host=MYSQL_HOST, 
        user=MYSQL_USER, 
        password=MYSQL_PASSWORD, 
        db=MYSQL_DB, 
        port=int(MYSQL_PORT)
    )
    cursor = db.cursor()
except Exception as e:
    print("Error connecting to database:", e)
    exit(1)

app = Flask(__name__)

# jwt_server = "http://127.0.0.1:8002/auth"


def user_exists(username):
    """Check if a user already exists in the database."""
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = %s", (username,))
    return cursor.fetchone()[0] > 0


@app.route('/users', methods=['POST'])
def user_register():
    """
    User Registration:
        - 201: User created successfully
        - 409: Username already exists
    """
    user = request.get_json()
    
    # Validate request data
    if 'username' not in user or 'password' not in user:
        return jsonify({"error": "Invalid request"}), 400

    username = user['username']
    
    if user_exists(username):
        return jsonify({"error": "Username already exists"}), 409
    else:
        hashed_password = bcrypt.hashpw(user['password'].encode(), bcrypt.gensalt())
        cursor.execute("INSERT INTO users (username, hashed_password) VALUES (%s, %s)", (username, hashed_password))
        db.commit()
        return jsonify({"message": "User added successfully"}), 201


@app.route('/users/login', methods=['POST'])
def user_login():
    """
    User Login:
        - 200: Login successful, returns JWT token
        - 403: Username not found or incorrect password
    """
    user = request.get_json()
    
    # Validate request data
    if 'username' not in user or 'password' not in user:
        return jsonify({"error": "Invalid request"}), 400

    username = user['username']

    cursor.execute("SELECT hashed_password FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()

    if not result:
        return jsonify({"error": "Username not found"}), 403

    hashed_password = result[0]

    if bcrypt.checkpw(user['password'].encode(), hashed_password.encode()):
        jwt_request = requests.post(JWT_SERVER, json={'username': username}).json()
        token = jwt_request.get('token')
        return jsonify({"message": "Login successful", "token": token}), 200
    else:
        return jsonify({"error": "Incorrect password"}), 403


@app.route('/users', methods=['PUT'])
def user_update_pwd():
    """
    Update User Password:
        - 200: Password updated successfully
        - 403: Username not found or incorrect password
    """
    user = request.get_json()

    # Validate request data
    if 'username' not in user or 'password' not in user or 'new_password' not in user:
        return jsonify({"error": "Invalid request"}), 400

    username = user['username']

    cursor.execute("SELECT hashed_password FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()

    if not result:
        return jsonify({"error": "Username not found"}), 403

    hashed_password = result[0]

    if bcrypt.checkpw(user['password'].encode(), hashed_password.encode()):
        new_hashed_password = bcrypt.hashpw(user['new_password'].encode(), bcrypt.gensalt())

        cursor.execute("UPDATE users SET hashed_password = %s WHERE username = %s", (new_hashed_password, username))
        db.commit()

        return jsonify({"message": "Password updated successfully"}), 200
    else:
        return jsonify({"error": "Incorrect password"}), 403


@app.route('/users/logout', methods=['POST'])
def user_logout():
    """
    User Logout:
        - 200: Logout successful
        - 403: Invalid token
    """
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"message": "Token required"}), 400
    
    jwt_request = requests.put(f"{JWT_SERVER}/logout", headers={'Authorization': token})

    if jwt_request.status_code == 200:
        return jsonify({"message": "Successfully logged out"}), 200
    else:
        return jsonify({"error": "Invalid token"}), 403


@app.route('/users/is_loggedin', methods=['POST'])
def user_is_loggedin():
    """
    Check if a user is logged in:
        - 200: User is logged in
        - 403: Invalid token or user not logged in
    """
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"error": "Token required"}), 400

    jwt_request = requests.post(f"{JWT_SERVER}/validate", headers={'Authorization': token})

    if jwt_request.status_code == 200:
        return jsonify({"message": "User is logged in"}), 200
    else:
        return jsonify({"error": "Invalid token"}), 403


@app.route('/health', methods=['GET'])
def health_check():
    """
    Kubernetes health check endpoint:
        - 200: Service is healthy
        - 500: Database connection issue
    """
    try:
        cursor.execute("SELECT 1")  # Check if MySQL connection is alive
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8001)

from flask import Flask, request, jsonify
import bcrypt
import requests

app = Flask(__name__)

jwt_server = "http://127.0.0.1:8002/auth"
users = {}

@app.route('/users', methods=['POST'])
def user_register():
    """
        201: created
        409: duplicate
    """
    user = request.get_json()
    
    # check if requests contains username and password
    if 'username' not in user or 'password' not in user:
        return jsonify({"error": "Invalid request"}), 400

    username = user['username']
    if username in users:
        return jsonify({"error": "Username already exists"}), 409
    else:
        users[username] = bcrypt.hashpw(user['password'].encode(), bcrypt.gensalt())
        return jsonify({"message": "User added successfully"}), 201
    
@app.route('/users/login', methods=['POST'])
def user_login():
    """
        200: OK
        403: forbidden
    """
    user = request.get_json()
    
    # check if requests contains username and password
    if 'username' not in user or 'password' not in user:
        return jsonify({"error": "Invalid request"}), 400

    username = user['username']
    if username not in users:
        return jsonify({"error": "Username not found"}), 403
    else:
        if bcrypt.checkpw(user['password'].encode(), users[username]):
            jwt_request = requests.post(f"{jwt_server}", json={'username': username}).json()
            token = jwt_request.get('token')
            return jsonify({"message": "Login successful", "token": token}), 200
        else:
            return jsonify({"error": "Incorrect password"}), 403
    
@app.route('/users', methods=['PUT'])
def user_update_pwd():
    """
        200: OK
        403: forbidden
    """
    user = request.get_json()
    
    # check if requests contains username and password
    if 'username' not in user or 'password' not in user or 'new_password' not in user:
        return jsonify({"error": "Invalid request"}), 400

    username = user['username']
    if username not in users:
        return jsonify({"error": "Username not found"}), 403
    else:
        if bcrypt.checkpw(user['password'].encode(), users[username]):
            users[username] = bcrypt.hashpw(user['new_password'].encode(), bcrypt.gensalt())
            return jsonify({"message": "Password updated successfully"}), 200
        else:
            return jsonify({"error": "Incorrect password"}), 403
    

if __name__ == '__main__':
    app.run(port=8001, debug=True)
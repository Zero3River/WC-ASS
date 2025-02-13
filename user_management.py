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
    user = request.get_json()
    
    # check if requests contains username and password
    if 'username' not in user or 'password' not in user or 'new_password' not in user:
        return jsonify({"error": "Invalid request"}), 400

    username = user['username']
    if username not in users:
        return jsonify({"error": "Username not found"}), 403
    else:
        if bcrypt.checkpw(user['password'].encode(), users[username]):
            # logout the user when password is updated
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({"message": "Token required"}), 400
            jwt_request = requests.put(f"{jwt_server}/logout", headers={'Authorization': token})
            if jwt_request.status_code != 200:
                return jsonify({"error": "Invalid token"}), 403
            # update password
            users[username] = bcrypt.hashpw(user['new_password'].encode(), bcrypt.gensalt())
            
            return jsonify({"message": "Password updated successfully"}), 200
        else:
            return jsonify({"error": "Incorrect password"}), 403
    

@app.route('/users/logout', methods=['POST'])
def user_logout():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"message": "Token required"}), 400
    
    print("logout token", token)
    jwt_request = requests.put(f"{jwt_server}/logout", headers={'Authorization': token})

    if jwt_request.status_code == 200:
        return jsonify({"message": "Successfully logged out"}), 200
    else:
        return jsonify({"error": "Invalid token"}), 403


@app.route('/users/logged_in', methods=['POST'])
def user_isLogin():
    print("AAAA")
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"message": "Token required"}), 400
    jwt_request = requests.post(f"{jwt_server}/validate", headers={'Authorization': token})
    if jwt_request.status_code == 200:
        return jsonify({"message": "User is logged in"}), 200
    else:
        return jsonify({"error": "Invalid token"}), 403
    

if __name__ == '__main__':
    app.run(port=8001)
from flask import Flask, request, jsonify
import base64
import hmac
import hashlib
import datetime
import json
from functools import wraps
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
blacklist = set()

def create_token(username):
    header = base64.urlsafe_b64encode(b'{"alg":"HS256","typ":"JWT"}').decode('utf-8').rstrip("=")
    payload_data = json.dumps({"username": username, "exp": int((datetime.datetime.utcnow() + datetime.timedelta(minutes=30)).timestamp())})
    payload = base64.urlsafe_b64encode(payload_data.encode('utf-8')).decode('utf-8').rstrip("=")
    signature = hmac.new(app.config['SECRET_KEY'].encode('utf-8'), f'{header}.{payload}'.encode('utf-8'), hashlib.sha256).digest()
    signature_b64 = base64.urlsafe_b64encode(signature).decode('utf-8').rstrip("=")
    return f'{header}.{payload}.{signature_b64}'

def verify_token(token):
    try:
        if token in blacklist:
            return None
        header, payload, signature = token.split('.')
        padding_needed = 4 - (len(payload) % 4) if len(payload) % 4 else 0
        
        signature_check = hmac.new(app.config['SECRET_KEY'].encode('utf-8'), f'{header}.{payload}'.encode('utf-8'), hashlib.sha256).digest()
        payload += "=" * padding_needed  
        if base64.urlsafe_b64encode(signature_check).decode('utf-8').rstrip("=") != signature:
            return None
        payload_data = base64.urlsafe_b64decode(payload + "=").decode('utf-8')
        payload_json = json.loads(payload_data)
        if datetime.datetime.utcnow().timestamp() > payload_json['exp']:
            return None
        return payload_json
    except Exception:
        return None

@app.route('/auth', methods=['POST'])
def auth():
    data = request.json
    username = data.get("username")
    if not username:
        return jsonify({"message": "Username is required"}), 400
    token = create_token(username)
    return jsonify({"username": username, "token": token})

@app.route('/auth/validate', methods=['POST'])
def validate():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"valid": False, "error": "Token missing"}), 401
    token = token.split()[1]
    user_data = verify_token(token)
    if not user_data:
        return jsonify({"valid": False, "error": "Token expired"}), 401
    return jsonify({"valid": True, "username": user_data["username"]}), 200

@app.route('/auth/logout', methods=['PUT'])
def logout():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"message": "Token required"}), 400
    token = token.split()[1]
    
    blacklist.add(token)

    return jsonify({"message": "Successfully logged out"}), 200


# Black list
if __name__ == '__main__':
    app.run(debug=True, port=8002)

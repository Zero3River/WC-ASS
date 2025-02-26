from flask import Flask, request, jsonify
import base64
import hmac
import hashlib
import datetime
import json
from functools import wraps
from dotenv import load_dotenv
import os
import redis

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
# Redis connection configuration
app.config['REDIS_HOST'] = os.getenv('REDIS_HOST', 'localhost')
app.config['REDIS_PORT'] = int(os.getenv('REDIS_PORT', 6379))
app.config['REDIS_DB'] = int(os.getenv('REDIS_DB', 0))
app.config['REDIS_PASSWORD'] = os.getenv('REDIS_PASSWORD', "redis")
app.config['TOKEN_BLACKLIST_PREFIX'] = 'token_blacklist:'
# Token expiration time in minutes - this will be used for both the token itself and the Redis entry
app.config['TOKEN_EXPIRATION'] = int(os.getenv('TOKEN_EXPIRATION', 30))

redis_client = redis.Redis(
    host=app.config['REDIS_HOST'],
    port=app.config['REDIS_PORT'],
    db=app.config['REDIS_DB'],
    password=app.config['REDIS_PASSWORD'],
    decode_responses=True  # Automatically decode responses to strings
)

def create_token(username):
    expiry_time = int((datetime.datetime.utcnow() + 
                    datetime.timedelta(minutes=app.config['TOKEN_EXPIRATION'])).timestamp())


    header = base64.urlsafe_b64encode(b'{"alg":"HS256","typ":"JWT"}').decode('utf-8').rstrip("=")
    payload_data = json.dumps({"username": username, "exp": expiry_time})
    payload = base64.urlsafe_b64encode(payload_data.encode('utf-8')).decode('utf-8').rstrip("=")
    signature = hmac.new(app.config['SECRET_KEY'].encode('utf-8'), f'{header}.{payload}'.encode('utf-8'), hashlib.sha256).digest()
    signature_b64 = base64.urlsafe_b64encode(signature).decode('utf-8').rstrip("=")
    return f'{header}.{payload}.{signature_b64}'

def is_token_blacklisted(token):
    """Check if a token is blacklisted in Redis"""
    return redis_client.exists(f"{app.config['TOKEN_BLACKLIST_PREFIX']}{token}")


def blacklist_token(token, user_data):
    """Add a token to the blacklist in Redis with an expiration time"""
    # Extract expiry time from token payload or use default
    exp_timestamp = user_data.get('exp', 
                                  int((datetime.datetime.utcnow() + 
                                      datetime.timedelta(minutes=app.config['TOKEN_EXPIRATION'])).timestamp()))
    
    # Calculate time to live in seconds
    current_timestamp = int(datetime.datetime.utcnow().timestamp())
    ttl = max(0, exp_timestamp - current_timestamp)
    
    # Store token in Redis with expiration
    redis_client.setex(
        f"{app.config['TOKEN_BLACKLIST_PREFIX']}{token}",
        ttl,
        "blacklisted"
    )

def verify_token(token):
    try:
        if is_token_blacklisted(token):
            return None
        header, payload, signature = token.split('.')
        padding_needed = 4 - (len(payload) % 4) if len(payload) % 4 else 0
        
        signature_check = hmac.new(app.config['SECRET_KEY'].encode('utf-8'), f'{header}.{payload}'.encode('utf-8'), hashlib.sha256).digest()
        if base64.urlsafe_b64encode(signature_check).decode('utf-8').rstrip("=") != signature:
            return None
        payload += "=" * padding_needed  
        payload_data = base64.urlsafe_b64decode(payload + "=").decode('utf-8')
        payload_json = json.loads(payload_data)
        if datetime.datetime.utcnow().timestamp() > payload_json['exp']:
            return None
        return payload_json
    except Exception as e:
        app.logger.error(f"Error verifying token: {e}")
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
    token = token.removeprefix("Bearer ")
    user_data = verify_token(token)
    if not user_data:
        return jsonify({"valid": False, "error": "Token expired"}), 401
    return jsonify({"valid": True, "username": user_data["username"]}), 200

@app.route('/auth/logout', methods=['PUT'])
def logout():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"message": "Token required"}), 400
    token = token.removeprefix("Bearer ")
    
    user_data = verify_token(token)
    if user_data:
        blacklist_token(token, user_data)
        return jsonify({"message": "Successfully logged out"}), 200
    else:
        return jsonify({"message": "Invalid token"}), 401

@app.route('/auth/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify Redis connection"""
    try:
        redis_client.ping()
        return jsonify({"status": "healthy", "redis": "connected"}), 200
    except redis.exceptions.ConnectionError:
        return jsonify({"status": "unhealthy", "redis": "disconnected"}), 503


# Black list
if __name__ == '__main__':
    app.run(port=8002, host='0.0.0.0')

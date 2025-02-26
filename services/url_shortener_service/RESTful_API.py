from flask import Flask, request, jsonify, Response
from hailstone import HailStone
import requests
import re
import redis
import os

app = Flask(__name__)

user_url_data = redis.StrictRedis(host='redis',port=6379, db=0, decode_responses=True, password=os.getenv('REDIS_PASSWORD', "redis")) # change the ip later

# JWT Authentication, get username from JWT token
def jwt_auth_user(headers):
    jwt_server = os.getenv('JWT_SERVER')
    response = requests.post(url=jwt_server, headers=headers)
    if response.status_code != 200:
        return None  # Authentication failed
    
    return response.json().get("username")

@app.route('/<id>', methods=['GET'])
def getURL(id):
    headers = request.headers
    username = jwt_auth_user(headers)
    if username is None:
        return jsonify({"error": "Forbidden"}), 403

    url_info = user_url_data.hgetall(id)
    stored_username = url_info.get('username')

    if url_info:
        stored_username = url_info.get('username')
        long_url = url_info.get('long_url')
        if username == stored_username:
            return jsonify({"value": long_url}), 301
        else:
            return jsonify({"error": "Forbidden"}), 403
    else:
        return jsonify({"error": "ID not found"}), 404

@app.route('/<id>', methods=['PUT'])
def updateURL(id):
    headers = request.headers
    username = jwt_auth_user(headers)

    if username is None:
        return jsonify({"error": "Forbidden"}), 403
    
    url_info = user_url_data.hgetall(id)
    stored_username = url_info.get('username')
    
    if url_info is None:
        return jsonify({"error": "ID not found"}), 404

    url = request.get_json(force=True).get('url')

    if not url or not checkURLValidity(url):
        return jsonify({"error": "Invalid URL"}), 400
    elif username != stored_username:
        return jsonify({"error": "Forbidden"}), 403
    
    user_url_data.hset(id, "long_url", url)

    return jsonify({"message": "Updated successfully"}), 200

@app.route('/<id>', methods=['DELETE'])
def deleteURL(id):
    headers = request.headers
    username = jwt_auth_user(headers)

    if username is None:
        return jsonify({"error": "Forbidden"}), 403
    
    urlinfo = user_url_data.hgetall(id)
    
    if urlinfo is None:
        return jsonify({"error": "ID not found"}), 404

    stored_username = urlinfo.get('username')
    
    if username != stored_username:
        return jsonify({"error": "Forbidden"}), 403

    user_url_data.delete(id)
    return Response(status=204)

@app.route('/', methods=['GET'])
def getURLs():
    headers = request.headers
    username = jwt_auth_user(headers)
    user_urls = user_url_data.smembers(username)
    
    if username is None:
        return jsonify({"error": "Forbidden"}), 403

    return jsonify({"keys": [element for element in user_urls]}), 200

@app.route('/', methods=['POST'])
def putURL():
    headers = request.headers
    
    username = jwt_auth_user(headers)

    if username is None:
        return jsonify({"error": "Forbidden"}), 403

    url = request.get_json().get('value')

    if not url or not checkURLValidity(url):
        return jsonify({"error": "Invalid URL"}), 400

    id = shortenURL(url)

    user_url_data.hset(id, mapping={"username": username, "long_url": url})
    user_url_data.sadd(username, id)

    return jsonify({"id": id}), 201

@app.route('/', methods=['DELETE'])
def deleteAll():
    headers = request.headers
    username = jwt_auth_user(headers)

    if username is None:
        return jsonify({"error": "Forbidden"}), 403

    deleteAllUrl(username)

    return Response(status=404)

def shortenURL(url):
    global hs
    return hs.generate()

def checkURLValidity(url):
    url_regex = r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
    return re.match(url_regex, url)

def deleteAllUrl(username):
    user_ids = user_url_data.smembers(username)
    if user_ids is None:
        return
    for id in user_ids:
        user_url_data.delete(id)
    user_url_data.delete(username)

if __name__ == '__main__':
    hs = HailStone(0)
    app.run(port=8000, host="0.0.0.0")

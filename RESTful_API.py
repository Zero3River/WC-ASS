from flask import Flask, request, jsonify, Response
from hailstone import HailStone
import requests
import re

app = Flask(__name__)

user_url_dict = {}  # Stores user-specific shortened URLs

# JWT Authentication, get username from JWT token
def jwt_auth_user(headers):
    jwt_server = "http://127.0.0.1:8002/auth/validate"
    #TODO Fix this part
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

    url_dict = user_url_dict.get(username, {})
    
    if id in url_dict:
        return jsonify({"value": url_dict[id]}), 301
    else:
        return jsonify({"error": "ID not found"}), 404

@app.route('/<id>', methods=['PUT'])
def updateURL(id):
    headers = request.headers
    username = jwt_auth_user(headers)

    if username is None:
        return jsonify({"error": "Forbidden"}), 403

    url_dict = user_url_dict.get(username)

    if url_dict is None or id not in url_dict:
        return jsonify({"error": "ID not found"}), 404

    url = request.get_json(force=True).get('url')

    if not url or not checkURLValidity(url):
        return jsonify({"error": "Invalid URL"}), 400

    url_dict[id] = url
    return jsonify({"message": "Updated successfully"}), 200

@app.route('/<id>', methods=['DELETE'])
def deleteURL(id):
    headers = request.headers
    username = jwt_auth_user(headers)

    if username is None:
        return jsonify({"error": "Forbidden"}), 403

    url_dict = user_url_dict.get(username, {})

    if id in url_dict:
        del url_dict[id]
        return Response(status=204)
    
    return jsonify({"error": "ID not found"}), 404

@app.route('/', methods=['GET'])
def getURLs():
    headers = request.headers
    username = jwt_auth_user(headers)

    if username is None:
        return jsonify({"error": "Forbidden"}), 403

    url_dict = user_url_dict.get(username)
    return jsonify({"keys": list(url_dict.keys())}), 200

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

    if username not in user_url_dict:
        user_url_dict[username] = {}

    user_url_dict[username][id] = url

    return jsonify({"id": id}), 201

@app.route('/', methods=['DELETE'])
def deleteAll():
    headers = request.headers
    username = jwt_auth_user(headers)

    if username is None:
        return jsonify({"error": "Forbidden"}), 403

    if username in user_url_dict:
        user_url_dict[username].clear()

    return Response(status=404)

def shortenURL(url):
    global hs
    return hs.generate()

def checkURLValidity(url):
    url_regex = r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
    return re.match(url_regex, url)

if __name__ == '__main__':
    hs = HailStone(0)
    app.run(port=8000)

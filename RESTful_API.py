from flask import Flask, request, jsonify, Response
from hailstone import HailStone
import re

app = Flask(__name__)
url_dict = {}

@app.route('/<id>', methods=['GET'])
def getURL(id):
    if id in url_dict:
        return jsonify({"value": url_dict[id]}), 301
    else:
        return jsonify({"error": "ID not found"}), 404

@app.route('/<id>', methods=['PUT'])
def updateURL(id):
    url = request.get_json(force=True)['url']
    
    if id in url_dict:
        if not checkURLValidity(url):
            return jsonify({"error": "Invalid URL"}), 400
        url_dict[id] = url
        return jsonify({"message": "Updated successfully"}), 200
    elif id not in url_dict:
        return jsonify({"error": "ID not found"}), 404

@app.route('/<id>', methods=['DELETE'])
def deleteURL(id):
    if id in url_dict:
        url_dict.pop(id)
        return Response(status=204)
    else:
        return jsonify({"error": "ID not found"}), 404

@app.route('/', methods=['GET'])
def getURLs():
    return jsonify({"keys": list(url_dict.keys())}), 200

@app.route('/', methods=['POST'])
def putURL():
    url = request.get_json()['value']
    if url is None or url == "" or not checkURLValidity(url):
        return jsonify({"error": "Invalid URL"}), 400
    else:
        id = shortenURL(url)
        url_dict[id] = url
        return jsonify({"id": id}), 201

@app.route('/', methods=['DELETE'])
def deleteAll():
    url_dict.clear()
    return Response(status=404)


def shortenURL(url):
    # url += str(time.time())
    # id = base64.b64encode(url.encode()).decode()
    # return id[-6:]
    global hs
    return hs.generate()

def checkURLValidity(url):
    # urlRegx = r"(http|https)://[a-zA-Z0-9\./]+"
    urlRegx = r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
    # https://stackoverflow.com/questions/3809401/what-is-a-good-regular-expression-to-match-a-url
    return re.match(urlRegx, url)


if __name__ == '__main__':
    hs = HailStone(0)
    app.run(port=8000)
    
    
import redis

user_url_data = redis.StrictRedis(host='an-pan.me',port=6379, db=5) # change the ip later

user1 = "user1"

user_url_data.hset("bdsfdsi", mapping={"username": user1, "long_url": "https://www.google.com"})
user_url_data.sadd(user1, "dbfsdbf")

print(user_url_data.hgetall("bdsfdsi"))
print(user_url_data.smembers(user1))

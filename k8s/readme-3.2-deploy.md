# Create namespace

```shell
kubectl apply -f namespace.yaml
```
# Apply configmaps and secrets first
```shell
kubectl apply -f config/ -n url-shortener
```
# MYSQL single
```shell
kubectl apply -f mysql/deploy-single.yaml -n url-shortener

kubectl run -n url-shortener -it --rm --image=mysql:5.6 --restart=Never mysql-client -- mysql -h mysql -psakila

kubectl get all -n url-shortener
```

<!-- # MySQL cluster

This is an alternative way of deploy mysql service using the official mysql operator, but be aware might run into version problems.

kubectl apply -f mysql/deploy-crds.yaml -n url-shortener

kubectl apply -f mysql/deploy-operator.yaml 

-->

# Wait for operator services to be ready


use this check progress

```shell
kubectl get all -n mysql-operator

kubectl apply -f config/mysql-secrets.yaml -n url-shortener

kubectl apply -f mysql/deploy-db.yaml -n url-shortener
```
# Wait for MySQL to be ready

Then use the following command to create a mysql shell and excute the initilization SQL

```shell
kubectl run --rm -it myshell -n url-shortener --image=container-registry.oracle.com/mysql/community-operator -- mysqlsh root:sakila@mysql-cluster --sql
```

```sql
CREATE DATABASE users;

CREATE TABLE users.users (
user_id INT AUTO_INCREMENT PRIMARY KEY,  
 username VARCHAR(255) NOT NULL UNIQUE,  
 hashed_password VARCHAR(255) NOT NULL
);
```

# apply redis

kubectl apply -f stateful-services/redis.yaml -n url-shortener

# apply apps

kubectl apply -f apps/ -n url-shortener

# apply ingress

kubectl apply -f ingress.yaml -n url-shortener

# get ingress ip and copy to hosts file

kubectl get ingress -n url-shortener

| NAME | CLASS | HOSTS | ADDRESS | PORTS | AGE |
|------|-------|--------|---------|-------|-----|
| url-shortener-ingress | nginx | wcassurl.com | xxx | 80 | 43s |

## For macos

sudo nano /private/etc/hosts

## For linux

sudo nano /etc/hosts

# test create user
```shell
curl -v -X POST http://wcassurl.com:<port>/users -H "Content-Type: application/json" -d '{
"username": "username",
"password": "password"
}'
```

# test login user
```shell
curl -v -X POST http://wcassurl.com:<port>/users/login -H "Content-Type: application/json" -d '{
"username": "username",
"password": "password"
}'
```


minikube addons enable ingress
minikube image load docker.io/library/wc-ass-url:latest
minikube image load docker.io/library/wc-ass-jwt:latest
minikube image load docker.io/library/wc-ass-user_management:latest
# Create namespace
kubectl apply -f namespace.yaml

# Apply configmaps and secrets first
kubectl apply -f config/ -n url-shortener

# MYSQL single

kubectl apply -f mysql/deploy-single.yaml -n url-shortener

kubectl run -it --rm --image=mysql:5.6 --restart=Never mysql-client -- mysql -h mysql -p sakila 


# MySQL cluster

kubectl apply -f mysql/deploy-crds.yaml -n url-shortener

kubectl apply -f mysql/deploy-operator.yaml

# Wait for operator services to be ready
echo "Waiting for stateful services to start..."

<!--use this check progress-->
kubectl get all -n mysql-operator 
<!-- kubectl wait --for=condition=ready deployment.apps/mysql-operator -n mysql-operator --timeout=120s -->

kubectl apply -f config/mysql-secrets.yaml -n url-shortener

kubectl apply -f mysql/deploy-db.yaml -n url-shortener

# Wait for MySQL to be ready
echo "Waiting for MySQL to start..."




kubectl run --rm -it myshell -n url-shortener  --image=container-registry.oracle.com/mysql/community-operator -- mysqlsh root:sakila@mysql-cluster --sql


CREATE DATABASE users;

CREATE TABLE users.users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,  
    username VARCHAR(255) NOT NULL UNIQUE,    
    hashed_password VARCHAR(255) NOT NULL
);

# apply redis 

kubectl apply -f stateful-services/redis.yaml -n url-shortener


# apply apps

kubectl apply -f apps/ -n url-shortener

# apply ingress
kubectl apply -f ingress.yaml -n url-shortener

# get ingress ip and copy to hosts file

kubectl get ingress -n url-shortener 
NAME                    CLASS   HOSTS          ADDRESS        PORTS   AGE
url-shortener-ingress   nginx   wcassurl.com   192.168.49.2   80      43s

# For macos

sudo nano /private/etc/hosts


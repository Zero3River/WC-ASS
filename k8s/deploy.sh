#!/bin/bash
# Create namespace
kubectl apply -f namespace.yaml

# Apply configmaps and secrets first
kubectl apply -f config/ -n url-shortener

# Apply stateful services next
kubectl apply -f stateful-services/ -n url-shortener

# Wait for stateful services to be ready
echo "Waiting for stateful services to start..."
kubectl wait --for=condition=ready pod -l app=mysql -n url-shortener --timeout=120s
kubectl wait --for=condition=ready pod -l app=redis -n url-shortener --timeout=120s

# Apply deployments last
kubectl apply -f apps/ -n url-shortener

echo "Deployment complete!"
# build image

# services=("jwt_service" "url_shortener_service" "user_management_service")
services=()

for service in "${services[@]}"; do
    docker build -f services/${service}/Dockerfile -t group8_${service}:latest services/${service}
done
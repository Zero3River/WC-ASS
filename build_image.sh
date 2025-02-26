# build image

# services=("jwt_service" "url_shortener_service" "user_management_service")
services=("jwt_service" "url_shortener_service" "user_management_service")

for service in "${services[@]}"; do
    docker build --no-cache -f services/${service}/Dockerfile -t group8_${service}:latest services/${service}
done
docker-compose -f docker-compose-hadoop.yml down -v

docker volume prune -f
docker network prune -f
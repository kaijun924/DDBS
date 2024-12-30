### Cleanup and Reset
for file in *docker-compose*.yml; do
  docker-compose -f "$file" down -v --remove-orphans
done
docker volume prune -f
docker network prune -f
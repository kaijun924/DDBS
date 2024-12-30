docker network create --driver bridge mongo_cluster_net
docker network create --driver bridge hadoop_cluster_net
docker network create --driver bridge redis_net

docker-compose -f 1_docker-compose_mongo_configsvr.yml up -d
docker-compose -f 5_docker-compose_redis.yml up -d
docker-compose -f 2_docker-compose_mongo_shards.yml up -d 
sleep 5
docker exec configsvr_a mongosh setup.js
docker exec dbms1_a mongosh setup.js
docker exec dbms2_a mongosh setup.js
docker-compose -f 3_docker-compose_mongo_router.yml up -d
docker-compose -f 6_docker_compose_monitor.yml up -d
sleep 15
docker exec router mongosh setup.js


##down
for file in *docker-compose*.yml; do
  docker-compose -f "$file" down -v --remove-orphans
done
docker volume prune -f
docker network prune -f
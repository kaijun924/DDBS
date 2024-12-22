docker network create --driver bridge mongo_cluster_net
docker network create --driver bridge hadoop

## mongo configsvr
docker-compose -f 1_docker-compose_mongo_configsvr.yml up -d
docker-compose -f 2_docker-compose_mongo_shards.yml up -d # TEMP：
sleep 5
docker exec configsvr_a mongosh setup.js
## check 
# docker exec configsvr_a mongosh --eval "rs.status()"

## mongo shards
# TEMP：docker-compose -f 2_docker-compose_mongo_shards.yml up -d
# TEMP：sleep 5
docker exec dbms1_a mongosh setup.js
docker exec dbms2_a mongosh setup.js
# docker exec dbmsX_a mongosh setup.js
## check
# docker exec dbms1_a mongosh --eval "rs.status()"

## mongo router
docker-compose -f 3_docker-compose_mongo_router.yml up -d
sleep 15
docker exec router mongosh setup.js
## check accessibility
# docker exec -it router bash
# mongosh configsvr_a:27017
# mongosh dbms1_a:27017
# mongosh dbms2_b:27017

## debug and dev
# docker exec -it router mongosh

# use admin
# db.createUser(
#     {
#         user: "monitor",
#         pwd: "monitor",
#         roles: [{ 
#             role: "clusterMonitor", 
#             db: "admin" 
#         },{ 
#             role: "read", 
#             db: "local" 
#         }]
#     })

docker-compose -f 4_docker-compose_hadoop.yml up -d
# wait until healthcheck is "healthy"
docker exec -it namenode /setup.sh
## View Hadoop Usage: http://localhost:9870/dfshealth.html#tab-datanode

docker-compose -f 5_docker-compose_redis.yml up -d

## Monitor
docker-compose -f 6_docker_compose_monitor.yml up -d


### Cleanup and Reset
for file in *docker-compose*.yml; do
  docker-compose -f "$file" down -v --remove-orphans
done
docker volume prune -f
docker network prune -f

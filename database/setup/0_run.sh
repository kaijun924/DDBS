docker network create --driver bridge mongo_cluster_net
docker network create --driver bridge hadoop_cluster_net
docker network create --driver bridge redis_net

## mongo configsvr
docker-compose -f 1_docker-compose_mongo_configsvr.yml up -d
docker-compose -f 2_docker-compose_mongo_shards.yml up -d
docker-compose -f 4_docker-compose_hadoop.yml up -d
docker-compose -f 5_docker-compose_redis.yml up -d
sleep 15
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
sleep 25
docker exec router mongosh setup.js
sleep 25
docker exec -it namenode /loading.sh
## View Hadoop Usage: http://localhost:9870/dfshealth.html#tab-datanode

# TEMP：docker-compose -f 5_docker-compose_redis.yml up -d

## Monitor
docker-compose -f 6_docker_compose_monitor.yml up -d
# http://localhost:3000 > opstree-mongodb-dashboard
docker-compose -f 1_docker-compose_mongo_configsvr.yml up -d
sleep 5
docker exec configsvr_a mongosh setup.js
docker-compose -f 2_docker-compose_mongo_shards.yml up -d 
docker exec dbms1_a mongosh setup.js
docker exec dbms2_a mongosh setup.js
docker-compose -f 3_docker-compose_mongo_router.yml up -d
sleep 15
docker exec router mongosh setup.js

##down
docker-compose -f 1_docker-compose_mongo_configsvr.yml down -v --remove-orphans
docker-compose -f 2_docker-compose_mongo_shards.yml down -v --remove-orphans
docker-compose -f 3_docker-compose_mongo_router.yml down -v --remove-orphans 
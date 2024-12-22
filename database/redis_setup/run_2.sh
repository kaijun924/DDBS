docker-compose -f docker-compose.yml up -d
# redis-cli -h 172.19.44.50 -p 6379
# CONFIG SET maxmemory 100mb
# CONFIG SET maxmemory-policy allkeys-lru

docker-compose -f docker-compose.yml down -v

docker network prune -f
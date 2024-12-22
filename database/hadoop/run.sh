docker network create --driver bridge hadoop
docker-compose -f docker-compose-hadoop.yml up -d

#等到docker ps全部状态 的状态是healthy
sleep 60
#首先，进入NameNode容器：
docker exec -it namenode bash
sudo service docker start
#启动config
docker-compose -f database/config/docker-compose.yml up -d
mongosh mongodb://localhost:40001
rs.initiate(
  {
    _id: "cfgrs",
    configsvr: true,
    members: [
      { _id : 0, host : "172.26.46.90:40001" },
      { _id : 1, host : "172.26.46.90:40002" }
    ]
  }
)

#启动分片
docker-compose -f database/shards/docker-compose.yml up -d

mongosh mongodb://localhost:50001
rs.initiate(
  {
    _id : "shard0",
    members: [
      { _id : 0, host : "172.26.46.90:50001" }
    ]
  }
)

mongosh mongodb://localhost:50002
rs.initiate(
  {
    _id : "shard1",
    members: [
      { _id : 0, host : "172.26.46.90:50002" }
    ]
  }
)

mongosh mongodb://localhost:50003
rs.initiate(
  {
    _id : "shard2",
    members: [
      { _id : 0, host : "172.26.46.90:50003" }
    ]
  }
)

mongosh mongodb://localhost:50004
rs.initiate(
  {
    _id : "shard3",
    members: [
      { _id : 0, host : "172.26.46.90:50004" }
    ]
  }
)
#开始router
docker-compose -f database/router/docker-compose.yml up -d
mongosh mongodb://localhost:60000

#添加分片
sh.addShard("shard0/172.26.46.90:50001")
sh.addShard("shard1/172.26.46.90:50002")
sh.addShard("shard2/172.26.46.90:50003")
sh.addShard("shard3/172.26.46.90:50004")
#create the zones
sh.addShardToZone("shard0", "DBMS1")
sh.addShardToZone("shard1", "DBMS1")
sh.addShardToZone("shard2", "DBMS2")
sh.addShardToZone("shard3", "DBMS2")

use demo
sh.enableSharding("demo")

sh.shardCollection("demo.user_beijing", { "uid" : 1 } )
sh.addTagRange( 
  "demo.user_beijing",
  { "uid" : MinKey },
  { "uid" : MaxKey }, 
  "DBMS1"
)

sh.shardCollection("demo.user_hongkong", { "uid" : 1 } )
sh.addTagRange( 
  "demo.user_hongkong",
  { "uid" : MinKey },
  { "uid" : MaxKey }, 
  "DBMS2"
)

#目前DBMS12有点奇怪

#清理
docker-compose -f database/config/docker-compose.yml down -v
docker-compose -f database/shards/docker-compose.yml down -v
docker-compose -f database/router/docker-compose.yml down -v






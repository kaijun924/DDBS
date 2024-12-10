docker exec -it router mongosh

// check shard status
sh.status();

// check shard infomation
db.adminCommand({ listShards: 1 });

// Show Zones
use config;
db.tags.find();



show dbs
user DBS
show collections
DBS.COLLECTION.stats()
DBS.COLLECTION.getShardDistribution()

// try query
db.collections.find({ _id: "yourDatabaseName.yourCollectionName" });
db.getCollectionNames()

use userDatabase
db.User.getShardDistribution()
db.User.countDocuments()
db.User.stats()

use articleDatabase
db.Article.getShardDistribution()
db.Article.stats()
db.Article.drop()

use readDatabase
db.Read.getShardDistribution()
db.Read.stats()
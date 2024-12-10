sh.addShard("dbms1_rs/dbms1_a:27017,dbms1_b:27017");
sh.addShard("dbms2_rs/dbms2_a:27017,dbms2_b:27017");
// sh.addShard("dbmsX_rs/dbmsX_a:27017,dbmsX_b:27017");
sh.addShardToZone("dbms1_rs", "DBMS1")
sh.addShardToZone("dbms2_rs", "DBMS2")
// sh.addShardToZone("dbmsX_rs", "DBMSX")

// Enable sharding for databases
sh.enableSharding("userDatabase");
sh.enableSharding("articleDatabase");
sh.enableSharding("readDatabase");
sh.enableSharding("beReadDatabase");
sh.enableSharding("popularRankDatabase");

// User Table Sharding
sh.shardCollection("userDatabase.User", { region: 1 });

// Tag ranges for regions
sh.addTagRange(
    "userDatabase.User",
    { region: "Beijing" },
    { region: "Beijing\0" },
    "DBMS1"
);

sh.addTagRange(
    "userDatabase.User",
    { region: "Hong Kong" },
    { region: "Hong Kong\0" },
    "DBMS2"
);

// Article Table Sharding
sh.shardCollection("articleDatabase.Article", { category: 1, shardCopy: 1 });

// Tag range for "technology" in DBMS2
sh.addTagRange(
    "articleDatabase.Article",
    { category: "technology"},
    { category: "technology\0"},
    "DBMS2"
);

// Tag ranges for "science" to duplicate across DBMS1 and DBMS2
sh.addTagRange(
    "articleDatabase.Article",
    { category: "science", shardCopy: 1 },
    { category: "science", shardCopy: 2 },
    "DBMS1"
);

sh.addTagRange(
    "articleDatabase.Article",
    { category: "science", shardCopy: 2 },
    { category: "science", shardCopy: 3 },
    "DBMS2"
);



// Read Table Sharding
sh.shardCollection("readDatabase.Read", { region: 1 });

// Tag ranges for regions (mirroring the User table)
sh.addTagRange(
    "readDatabase.Read",
    { region: "Beijing" },
    { region: "Beijing\0" },
    "DBMS1"
);

sh.addTagRange(
    "readDatabase.Read",
    { region: "Hong Kong" },
    { region: "Hong Kong\0" },
    "DBMS2"
);

// Be-Read Table Sharding
sh.shardCollection("beReadDatabase.BeRead", { shardCopy: 1 });

// Science in Both DBMS1 and DBMS2
sh.addTagRange(
    "beReadDatabase.BeRead",
    { shardCopy: 1 },
    { shardCopy: 2 },
    "DBMS1"
);

sh.addTagRange(
    "beReadDatabase.BeRead",
    { shardCopy: 2 },
    { shardCopy: 3 },
    "DBMS2"
);

// Popular-Rank Table Sharding
sh.shardCollection("popularRankDatabase.PopularRank", { temporalGranularity: 1 });

// Tag ranges for granularity
sh.addTagRange(
    "popularRankDatabase.PopularRank",
    { temporalGranularity: "daily" },
    { temporalGranularity: "daily\0" },
    "DBMS1"
);

sh.addTagRange(
    "popularRankDatabase.PopularRank",
    { temporalGranularity: "weekly" },
    { temporalGranularity: "weekly\0" },
    "DBMS2"
);

sh.addTagRange(
    "popularRankDatabase.PopularRank",
    { temporalGranularity: "monthly" },
    { temporalGranularity: "monthly\0" },
    "DBMS2"
);

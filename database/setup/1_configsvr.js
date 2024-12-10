rs.initiate({
    _id: "cfgrs",
    configsvr: true,
    members: [
        { _id: 0, host: 'configsvr_a:27017' },
        { _id: 1, host: 'configsvr_b:27017' },
        { _id: 2, host: 'configsvr_c:27017' }
    ]
});
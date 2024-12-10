rs.initiate({
    _id: "dbmsX_rs",
    members: [
        { _id: 0, host: "dbmsX_a:27017" },
        { _id: 1, host: "dbmsX_b:27017" }
    ]
});
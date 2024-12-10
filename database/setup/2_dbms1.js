rs.initiate({
    _id: "dbms1_rs",
    members: [
        { _id: 0, host: "dbms1_a:27017" },
        { _id: 1, host: "dbms1_b:27017" }
    ]
});
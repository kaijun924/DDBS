rs.initiate({
    _id: "dbms2_rs",
    members: [
        { _id: 0, host: "dbms2_a:27017" },
        { _id: 1, host: "dbms2_b:27017" }
    ]
});
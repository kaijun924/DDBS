import React, { useEffect, useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import "./UserList.css"; // Import CSS styles

function UserList() {
  const [users, setUsers] = useState([]);

  // Fetch user data from API
  useEffect(() => {
    axios
      .get("http://localhost:8000/users")
      .then((response) => {
        setUsers(response.data);
      })
      .catch((error) => {
        console.error("Error fetching user data:", error);
      });
  }, []);

  return (
    <div>
      <h1>User List</h1>
      <table border="1" style={{ width: "100%", textAlign: "left", borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <th>UID</th>
            <th>Name</th>
            <th>Gender</th>
            <th>Email</th>
            <th>Phone</th>
            <th>Department</th>
            <th>Grade</th>
            <th>Language</th>
            <th>Region</th>
            <th>Role</th>
            <th>Preferred Tags</th>
            <th>Obtained Credits</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr key={user.uid} className="table-row">
              <td>
                <Link to={`/user/${user.uid}`} style={{ textDecoration: "none", color: "blue" }}>
                  {user.uid}
                </Link>
              </td>
              <td>{user.name}</td>
              <td>{user.gender}</td>
              <td>{user.email}</td>
              <td>{user.phone}</td>
              <td>{user.dept}</td>
              <td>{user.grade}</td>
              <td>{user.language}</td>
              <td>{user.region}</td>
              <td>{user.role}</td>
              <td>{user.preferTags}</td>
              <td>{user.obtainedCredits}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default UserList;

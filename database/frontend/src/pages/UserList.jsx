import React, { useEffect, useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import { Container, Table } from "react-bootstrap";
import "./UserList.css"; // Import the CSS file

function UserList() {
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);

  // Fetch user data from API
  useEffect(() => {
    axios
      .get("http://localhost:8000/users") // Replace with your actual API endpoint
      .then((response) => {
        setUsers(response.data); // Store the fetched user data in state
      })
      .catch((error) => {
        console.error("Error fetching user data:", error);
      });
  }, []);

  // Handle row click
  const handleRowClick = (user) => {
    setSelectedUser(user.uid); // Set the selected row by user ID
    console.log("Selected User:", user); // Optional: log the selected user
  };

  return (
    <Container className="mt-4">
      <h1 className="mb-4">User List</h1>
      <Table striped bordered hover responsive>
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
            <tr key={user.uid}>
              <td>
                <Link to={`/user/${user.uid}`} className="text-primary text-decoration-none">
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
      </Table>
    </Container>
  );
}

export default UserList;

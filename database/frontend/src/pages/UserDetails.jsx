import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import { Link } from "react-router-dom";
import { Container, Table } from "react-bootstrap";
import "./UserDetails.css"; // Import custom styles

function UserDetails() {
  const { uid } = useParams(); // Extract 'uid' from the URL
  const [userData, setUserData] = useState(null);

  useEffect(() => {
    // Fetch user details and their reads
    axios
      .get(`http://localhost:8000/reads_by_user/${uid}`)
      .then((response) => {
        setUserData(response.data);
      })
      .catch((error) => {
        console.error("Error fetching user details:", error);
      });
  }, [uid]);

  if (!userData) {
    return <div>Loading user details...</div>;
  }

  const { user, reads } = userData;

  
  return (
    <Container className="mt-4">
      {/* User Info */}
      <h1 className="mb-4">User Details</h1>
      <div className="user-info mb-4">
        <p><strong>UID:</strong> {user.uid}</p>
        <p><strong>Name:</strong> {user.name}</p>
        <p><strong>Gender:</strong> {user.gender}</p>
        <p><strong>Email:</strong> {user.email}</p>
        <p><strong>Phone:</strong> {user.phone}</p>
        <p><strong>Department:</strong> {user.dept}</p>
        <p><strong>Grade:</strong> {user.grade}</p>
        <p><strong>Language:</strong> {user.language}</p>
        <p><strong>Region:</strong> {user.region}</p>
        <p><strong>Role:</strong> {user.role}</p>
        <p><strong>Preferred Tags:</strong> {user.preferTags}</p>
        <p><strong>Obtained Credits:</strong> {user.obtainedCredits}</p>
      </div>

      {/* Reads Table */}
      <h2 className="mb-4">Read History: (Total {reads.length})</h2>
      <Table striped bordered hover responsive>
        <thead>
          <tr>
            <th>ID</th>
            <th>Article ID</th>
            <th>Read Time (minutes)</th>
            <th>Agreed?</th>
            <th>Commented?</th>
            <th>Shared?</th>
            <th>Comment Details</th>
          </tr>
        </thead>
        <tbody>
          {reads.map((read) => (
            <tr key={read.id}>
              <td>{read.id}</td>
              <td>
                <Link to={`/article/${read.aid}`} className="text-primary text-decoration-none">
                  {read.aid}
                </Link>
              </td>
              <td>{read.readTimeLength}</td>
              <td>{read.agreeOrNot === "1" ? "Yes" : "No"}</td>
              <td>{read.commentOrNot === "1" ? "Yes" : "No"}</td>
              <td>{read.shareOrNot === "1" ? "Yes" : "No"}</td>
              <td>{read.commentDetail}</td>
            </tr>
          ))}
        </tbody>
      </Table>
    </Container>
  );
}

export default UserDetails;

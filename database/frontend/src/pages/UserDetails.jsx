import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";

function UserDetails() {
  const { id } = useParams();
  const [user, setUser] = useState(null);

  useEffect(() => {
    axios.get(`http://localhost:8000/users/${id}`)
      .then((response) => setUser(response.data))
      .catch((error) => console.error(error));
  }, [id]);

  if (!user) return <div>Loading...</div>;

  return (
    <div>
      <h1>{user.name}'s Details</h1>
      <p>Email: {user.email}</p>
      <p>Age: {user.age}</p>
    </div>
  );
}

export default UserDetails;

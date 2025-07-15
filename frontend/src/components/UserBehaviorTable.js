import React, { useEffect, useState } from "react";
import axios from "axios";

function UserBehaviorTable() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    axios.get("http://127.0.0.1:5000/user_behavior")
      .then(res => setUsers(res.data))
      .catch(console.error);
  }, []);

  if (users.length === 0) return <p>Loading user behavior…</p>;

  return (
    <div>
      <h2>User Behavior</h2>
      <table>
        <thead>
          <tr>
            <th>UUID</th>
            <th>Logs</th>
            <th>Unique Accounts</th>
            <th>Frauds</th>
            <th>Fraud Rate (%)</th>
          </tr>
        </thead>
        <tbody>
          {users.map(user => (
            <tr key={user.uuid}>
              <td>{user.uuid}</td>
              <td>{user.logs}</td>
              <td>{user.unique_accounts}</td>
              <td>{user.frauds}</td>
              <td>{user.fraud_rate}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default UserBehaviorTable;

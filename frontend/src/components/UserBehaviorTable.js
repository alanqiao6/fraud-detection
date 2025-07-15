import React from "react";

const UserBehaviorTable = ({ data }) => {
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
          {data.map((row) => (
            <tr key={row.uuid}>
              <td>{row.uuid}</td>
              <td>{row.logs}</td>
              <td>{row.unique_accounts}</td>
              <td>{row.frauds}</td>
              <td>{row.fraud_rate}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default UserBehaviorTable;

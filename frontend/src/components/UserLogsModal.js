import React, { useEffect, useState } from "react";
import axios from "axios";


const UserLogsModal = ({ uuid, onClose }) => {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    axios.get(`https://hack-attack-164352439456.us-central1.run.app/user_logs/${uuid}`)
    .then(res => setLogs(res.data))
      .catch(err => console.error(err));
  }, [uuid]);

  return (
    <div style={{
      position: "fixed",
      top: 0, left: 0, right: 0, bottom: 0,
      backgroundColor: "rgba(0,0,0,0.5)",
      display: "flex", alignItems: "center", justifyContent: "center"
    }}>
      <div style={{ background: "white", padding: "20px", maxHeight: "80%", overflowY: "auto" }}>
        <h2>Logs for {uuid}</h2>
        <button onClick={onClose}>Close</button>
        <table>
          <thead>
            <tr>
              {logs[0] && Object.keys(logs[0]).map(col => (
                <th key={col}>{col}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {logs.map((log, idx) => (
              <tr key={idx}>
                {Object.values(log).map((val, i) => (
                  <td key={i}>{val}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default UserLogsModal;

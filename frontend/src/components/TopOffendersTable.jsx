import React from "react";

const TopOffendersTable = ({ data }) => {
  if (!data || data.length === 0) return <p>No data available.</p>;

  // compute fraud frequency
  const processed = data.map(row => {
    const total = row.fraud + row.not_fraud;
    const frequency = total > 0 ? (row.fraud / total) * 100 : 0;
    return {
      country: row.shipFrom_countryCode,
      fraud: row.fraud,
      total,
      frequency,
    };
  });

  // sort descending by frequency
  const sorted = processed.sort((a, b) => b.frequency - a.frequency);

  return (
    <div className="card">
      <h2>Top Offending Countries</h2>
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <th style={{ textAlign: "left", padding: "8px" }}>Rank</th>
            <th style={{ textAlign: "left", padding: "8px" }}>Country</th>
            <th style={{ textAlign: "left", padding: "8px" }}>Fraud Count</th>
            <th style={{ textAlign: "left", padding: "8px" }}>Total Logs</th>
            <th style={{ textAlign: "left", padding: "8px" }}>Fraud Frequency (%)</th>
          </tr>
        </thead>
        <tbody>
          {sorted.map((row, idx) => (
            <tr key={row.country}>
              <td style={{ padding: "8px" }}>{idx + 1}</td>
              <td style={{ padding: "8px" }}>{row.country}</td>
              <td style={{ padding: "8px" }}>{row.fraud}</td>
              <td style={{ padding: "8px" }}>{row.total}</td>
              <td style={{ padding: "8px" }}>{row.frequency.toFixed(2)}%</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default TopOffendersTable;

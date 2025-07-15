import React, { useEffect, useState } from "react";
import axios from "axios";
import FraudBarChart from "../components/FraudBarChart";

const DashboardPage = () => {
  const [summary, setSummary] = useState(null);

  useEffect(() => {
    axios.get("http://127.0.0.1:5000/summary")
      .then(res => setSummary(res.data))
      .catch(err => console.error(err));
  }, []);

  if (!summary) return <p>Loading...</p>;

  return (
    <div style={{ padding: "20px" }}>
      <h1>Dashboard</h1>
      <FraudBarChart data={summary} />
    </div>
  );
};

export default DashboardPage;

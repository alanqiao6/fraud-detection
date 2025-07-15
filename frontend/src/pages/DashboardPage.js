import React, { useEffect, useState } from "react";
import axios from "axios";
import FraudBarChart from "../components/FraudBarChart";
import GeographyChart from "../components/GeographyChart";
import TimeTrendsChart from "../components/TimeTrendsChart";
import UserBehaviorTable from "../components/UserBehaviorTable";

const DashboardPage = () => {
  const [summary, setSummary] = useState(null);
  const [geo, setGeo] = useState([]);
  const [trends, setTrends] = useState([]);
  const [users, setUsers] = useState([]);

  useEffect(() => {
    axios.get("http://127.0.0.1:5000/summary").then(res => setSummary(res.data));
    axios.get("http://127.0.0.1:5000/geography").then(res => setGeo(res.data));
    axios.get("http://127.0.0.1:5000/time_trends").then(res => setTrends(res.data));
    axios.get("http://127.0.0.1:5000/user_behavior").then(res => setUsers(res.data));
  }, []);

  if (!summary) return <p>Loading...</p>;

  return (
    <div style={{ padding: "20px" }}>
      <h1>Dashboard</h1>
      <FraudBarChart data={summary} />
      <GeographyChart data={geo} />
      <TimeTrendsChart data={trends} />
      <UserBehaviorTable data={users} />
    </div>
  );
};

export default DashboardPage;

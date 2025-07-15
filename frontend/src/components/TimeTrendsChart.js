import React, { useEffect, useState } from "react";
import axios from "axios";
import { Line } from "react-chartjs-2";

function TimeTrendsChart() {
  const [trends, setTrends] = useState([]);

  useEffect(() => {
    axios.get("http://127.0.0.1:5000/time_trends")
      .then(res => setTrends(res.data))
      .catch(console.error);
  }, []);

  if (trends.length === 0) return <p>Loading time trends…</p>;

  const data = {
    labels: trends.map(t => t.date),
    datasets: [
      {
        label: "Fraud",
        data: trends.map(t => t.fraud),
        borderColor: "red",
        fill: false
      },
      {
        label: "Not Fraud",
        data: trends.map(t => t.not_fraud),
        borderColor: "green",
        fill: false
      }
    ]
  };

  return (
    <div>
      <h2>Time Trends</h2>
      <Line data={data} />
    </div>
  );
}

export default TimeTrendsChart;

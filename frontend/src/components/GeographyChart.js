import React, { useEffect, useState } from "react";
import axios from "axios";
import { Bar } from "react-chartjs-2";

function GeographyChart() {
  const [geo, setGeo] = useState([]);

  useEffect(() => {
    axios.get("http://127.0.0.1:5000/geography")
      .then(res => setGeo(res.data))
      .catch(console.error);
  }, []);

  if (geo.length === 0) return <p>Loading geography…</p>;

  const data = {
    labels: geo.map(g => g.shipFrom_countryCode),
    datasets: [
      {
        label: "Fraud",
        data: geo.map(g => g.fraud),
        backgroundColor: "red"
      },
      {
        label: "Not Fraud",
        data: geo.map(g => g.not_fraud),
        backgroundColor: "green"
      }
    ]
  };

  return (
    <div>
      <h2>Fraud by Geography</h2>
      <Bar data={data} />
    </div>
  );
}

export default GeographyChart;

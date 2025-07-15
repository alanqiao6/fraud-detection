import React from "react";
import { Bar } from "react-chartjs-2";

const GeographyChart = ({ data }) => {
  const labels = data.map(row => row.shipFrom_countryCode);
  const fraud = data.map(row => row.fraud);
  const notFraud = data.map(row => row.not_fraud);

  const chartData = {
    labels,
    datasets: [
      {
        label: "Fraud",
        data: fraud,
        backgroundColor: "#ef4444",
      },
      {
        label: "Not Fraud",
        data: notFraud,
        backgroundColor: "#10b981",
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      title: {
        display: true,
        text: "Fraud by Geography",
      },
    },
  };

  return <Bar data={chartData} options={options} />;
};

export default GeographyChart;

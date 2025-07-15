import React from "react";
import { Line } from "react-chartjs-2";

const TimeTrendsChart = ({ data }) => {
  const labels = data.map(row => row.date);
  const fraud = data.map(row => row.fraud);
  const notFraud = data.map(row => row.not_fraud);

  const chartData = {
    labels,
    datasets: [
      {
        label: "Fraud",
        data: fraud,
        borderColor: "#ef4444",
        fill: false,
      },
      {
        label: "Not Fraud",
        data: notFraud,
        borderColor: "#10b981",
        fill: false,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      title: {
        display: true,
        text: "Fraud over Time",
      },
    },
  };

  return <Line data={chartData} options={options} />;
};

export default TimeTrendsChart;

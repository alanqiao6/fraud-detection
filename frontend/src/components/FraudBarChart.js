import React from "react";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

// Register ONCE at the top level
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const FraudBarChart = ({ data }) => {
  const chartData = {
    labels: ["Fraud", "Not Fraud"],
    datasets: [
      {
        label: "Count",
        data: [data.fraud, data.not_fraud],
        backgroundColor: ["#ef4444", "#10b981"],
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: "top",
      },
      title: {
        display: true,
        text: "Fraud vs Not Fraud",
      },
    },
  };

  return <Bar data={chartData} options={options} />;
};

export default FraudBarChart;

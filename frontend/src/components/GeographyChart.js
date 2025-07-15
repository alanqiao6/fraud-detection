import React from "react";
import { Pie, Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  ArcElement,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
  Title,
} from "chart.js";

ChartJS.register(
  ArcElement,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
  Title
);

const GeographyChart = ({ data }) => {
  const labels = data.map((row) => row.shipFrom_countryCode);
  const fraudCounts = data.map((row) => row.fraud);

  const colors = [
    "#FFB500", "#301E14", "#E63946", "#457B9D", "#2A9D8F",
    "#F4A261", "#6A4C93", "#8D99AE", "#D90429", "#118AB2"
  ];

  const pieData = {
    labels,
    datasets: [
      {
        label: "Fraud Cases",
        data: fraudCounts,
        backgroundColor: colors.slice(0, labels.length),
      },
    ],
  };

  const pieOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      title: {
        display: true,
        text: "Fraud by Geography (Proportion)",
      },
      legend: {
        position: "right",
      },
    },
  };

  // Compute fraud frequency: fraud / (fraud + not_fraud)
  const fraudFrequencies = data.map((row) => {
    const total = row.fraud + row.not_fraud;
    return total > 0 ? (row.fraud / total) * 100 : 0; // in percent
  });

  const barData = {
    labels,
    datasets: [
      {
        label: "Fraud Frequency (%)",
        data: fraudFrequencies,
        backgroundColor: colors.slice(0, labels.length),
      },
    ],
  };

  const barOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      title: {
        display: true,
        text: "Fraud Frequency by Geography",
      },
      legend: {
        display: false,
      },
      tooltip: {
        callbacks: {
          label: (ctx) => `${ctx.parsed.y.toFixed(2)}%`,
        },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          callback: (val) => `${val}%`,
        },
        title: {
          display: true,
          text: "Fraud Frequency (%)",
        },
      },
    },
  };

  return (
    <div style={{
      display: "flex",
      gap: "20px",
      flexWrap: "wrap",
      justifyContent: "center"
    }}>
      <div style={{ width: "300px", height: "300px" }}>
        <Pie data={pieData} options={pieOptions} />
      </div>
      <div style={{ flex: "1 1 400px", height: "300px" }}>
        <Bar data={barData} options={barOptions} />
      </div>
    </div>
  );
};

export default GeographyChart;

import React, { useState } from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const TimeTrendsChartWithFilter = ({ data }) => {
  const [selectedCountry, setSelectedCountry] = useState("ALL");

  if (!data || data.length === 0) return <p>No data available.</p>;

  const countries = Array.from(new Set(data.map(d => d.country)));

  const filtered = selectedCountry === "ALL"
    ? data
    : data.filter(d => d.country === selectedCountry);

  const grouped = {};
  filtered.forEach(d => {
    if (!grouped[d.date]) grouped[d.date] = 0;
    grouped[d.date] += d.fraud;
  });

  const labels = Object.keys(grouped).sort();
  const counts = labels.map(date => grouped[date]);

  const chartData = {
    labels,
    datasets: [
      {
        label: `Fraud Cases (${selectedCountry})`,
        data: counts,
        borderColor: "#E63946",
        backgroundColor: "#F4A261",
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      title: {
        display: true,
        text: "Fraud Over Time",
      },
    },
  };

  return (
    <div className="card">
      <h2>Fraud Trends Over Time</h2>

      <div style={{ marginBottom: "10px" }}>
        <label>
          Select Country:{" "}
          <select
            value={selectedCountry}
            onChange={(e) => setSelectedCountry(e.target.value)}
          >
            <option value="ALL">All</option>
            {countries.map(c => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
        </label>
      </div>

      <div style={{ height: "300px" }}>
        <Line data={chartData} options={options} />
      </div>
    </div>
  );
};

export default TimeTrendsChartWithFilter;

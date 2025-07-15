import React, { useEffect, useState } from "react";
import axios from "axios";
import TimeTrendsChart from "../components/TimeTrendsChart";
import UserLogsModal from "../components/UserLogsModal";
import UserBehaviorTable from "../components/UserBehaviorTable";
import FraudMap from "../components/FraudMap";
import FraudBarChart from "../components/FraudBarChart";
import GeographyChart from "../components/GeographyChart";
import "./DashboardPage.css";
import TopOffendersTable from "../components/TopOffendersTable";
import TimeTrendsChartWithFilter from "../components/TimeTrendsChartWithFilter";
import { Link } from "react-router-dom";




const DashboardPage = () => {
  const [summary, setSummary] = useState(null);
  const [geoData, setGeoData] = useState([]);
  const [timeTrends, setTimeTrends] = useState([]);
  const [investigatingUuid, setInvestigatingUuid] = useState(null);

  useEffect(() => {
    axios.get("http://127.0.0.1:5000/summary")
      .then(res => setSummary(res.data))
      .catch(err => console.error(err));

    axios.get("http://127.0.0.1:5000/geography")
      .then(res => setGeoData(res.data))
      .catch(err => console.error(err));

    axios.get("http://127.0.0.1:5000/time_trends")
      .then(res => setTimeTrends(res.data))
      .catch(err => console.error(err));
  }, []);

  if (!summary) return <p>Loading dashboard...</p>;

  return (
    <div className="dashboard-page">
      {/* Top Bar */}
      <div className="topbar">
        <Link to="/">
            <img
            src="/static/images/ups.png"
            alt="UPS Logo"
            className="logo"
            style={{ cursor: "pointer" }}
            />
        </Link>
        <div className="header-text">
            <h1>UPS Fraud Detection Dashboard</h1>
            <p className="tagline">
            Built for secure log verification and anomaly detection
            </p>
        </div>
    </div>


      {/* Main Container */}
      <div className="container">
        <div className="card">
          <h2>Fraud Summary</h2>
          <div className="summary-stats">
            <div><strong>Fraudulent Logs:</strong> {summary.fraud}</div>
            <div><strong>Non-Fraudulent Logs:</strong> {summary.not_fraud}</div>
            <div><strong>Total Logs:</strong> {summary.total_logs}</div>
            <div><strong>Fraud Rate:</strong> {summary.fraud_rate}%</div>
          </div>
          <FraudBarChart data={summary} />
        </div>

        <div className="card">
          <h2>Fraud by Geography</h2>
          {geoData.length === 0 ? (
            <p>No fraud detected in any geography.</p>
          ) : (
            <GeographyChart data={geoData} />
          )}
        </div>

        <div className="card">
            <TopOffendersTable data={geoData} />
        </div>

        <div className="card">
          <h2>Fraud Map</h2>
          <FraudMap />
        </div>

        <div className="card">
          <h2>Time-based Trends</h2>
          <TimeTrendsChartWithFilter data={timeTrends} />
        </div>

        <div className="card">
          <h2>Flagged Users</h2>
          <UserBehaviorTable onInvestigate={setInvestigatingUuid} />
          {investigatingUuid && (
            <UserLogsModal
              uuid={investigatingUuid}
              onClose={() => setInvestigatingUuid(null)}
            />
          )}
        </div>
      </div>

      <footer>
        <p>© 2025 UPS Hackathon Team</p>
      </footer>
    </div>
  );
};

export default DashboardPage;

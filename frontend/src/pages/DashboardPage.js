import React, { useEffect, useState } from "react";
import axios from "axios";
import TimeTrendsChart from "../components/TimeTrendsChart";
import UserLogsModal from "../components/UserLogsModal";
import UserBehaviorTable from "../components/UserBehaviorTable";
import FraudMap from "../components/FraudMap";


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

  if (!summary) return <p>Loading...</p>;

  return (
    <div style={{ padding: "20px" }}>
      <h1>Dashboard</h1>

      <section>
        <h2>Fraud Summary</h2>
        <p>Fraudulent Logs: {summary.fraud}</p>
        <p>Non-Fraudulent Logs: {summary.not_fraud}</p>
        <p>Total Logs: {summary.total_logs}</p>
        <p>Fraud Rate: {summary.fraud_rate}%</p>
      </section>

      <section style={{ marginTop: "20px" }}>
        <h2>Fraud by Geography</h2>
        {geoData.length === 0 ? (
          <p>No fraud detected in any geography.</p>
        ) : (
          <ul>
            {geoData.map(row => (
              <li key={row.shipFrom_countryCode}>
                {row.shipFrom_countryCode}: {row.fraud} frauds
              </li>
            ))}
          </ul>
        )}
      </section>

      <section style={{ marginTop: "20px" }}>
        <FraudMap />
      </section>

      <section style={{ marginTop: "20px" }}>
        <h2>Time-based Trends</h2>
        <TimeTrendsChart data={timeTrends} />
      </section>

      <section style={{ marginTop: "20px" }}>
        <h2>Flagged Users</h2>
        <UserBehaviorTable onInvestigate={setInvestigatingUuid} />
        {investigatingUuid && (
          <UserLogsModal
            uuid={investigatingUuid}
            onClose={() => setInvestigatingUuid(null)}
          />
        )}
      </section>
    </div>
  );
};

export default DashboardPage;

import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "./UploadPage.css";

function UploadPage() {
  const [file, setFile] = useState(null);
  const [error, setError] = useState(null);
  const [fileName, setFileName] = useState("No file chosen");
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    setFileName(selectedFile ? selectedFile.name : "No file chosen");
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      await axios.post("https://hack-attack-164352439456.us-central1.run.app/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      navigate("/dashboard");
    } catch (err) {
      console.error(err);
      setError("Upload failed.");
    }
  };

  return (
    <div>
      {/* Top Bar */}
      <div className="topbar">
        <img
          src="/static/images/ups.png"
          alt="UPS Logo"
          className="logo"
        />
        <div className="header-text">
          <h1>UPS Fraud Detection System</h1>
          <p className="tagline">
            Built for secure log verification and anomaly detection
          </p>
        </div>
      </div>

      {/* Main Container */}
      <div className="container">
        <p className="instruction">
          Please upload a <strong>CSV file</strong> containing system logs and press{" "}
          <strong>Check</strong> to analyze.
        </p>

        <form onSubmit={handleUpload}>
          <label htmlFor="file-input" className="file-label">
            Choose CSV File
          </label>
          <input
            type="file"
            id="file-input"
            name="file"
            accept=".csv"
            hidden
            onChange={handleFileChange}
          />
          <span id="file-name">{fileName}</span>

          <button type="submit">Check</button>
        </form>

        {error && <div id="result" style={{ color: "red" }}>{error}</div>}
      </div>

      {/* Footer */}
      <footer>
        <p>© 2025 UPS Hackathon Team</p>
      </footer>
    </div>
  );
}

export default UploadPage;

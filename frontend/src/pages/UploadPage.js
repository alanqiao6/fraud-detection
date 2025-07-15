import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function UploadPage() {
  const [file, setFile] = useState(null);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);

    try {
      await axios.post("http://127.0.0.1:5000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      // Redirect to dashboard after successful upload
      navigate("/dashboard");
    } catch (err) {
      console.error(err);
      setError("Upload failed.");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Fraud Detection - Upload Logs</h1>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default UploadPage;

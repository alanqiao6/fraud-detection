import React, { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://127.0.0.1:5000/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setResult(res.data);
    } catch (err) {
      console.error(err);
      setResult({ error: "Upload failed" });
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Fraud Detection</h1>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>

      <div style={{ marginTop: "20px" }}>
        <h2>Result:</h2>
        <pre>{result ? JSON.stringify(result, null, 2) : "No result yet"}</pre>
      </div>
    </div>
  );
}

export default App;

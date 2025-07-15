import React, { useEffect, useState } from "react";
import { DataGrid } from "@mui/x-data-grid";
import axios from "axios";
import { BACKEND_URL } from "./config";


const UserBehaviorTable = ({ onInvestigate }) => {
  const [rows, setRows] = useState([]);

  useEffect(() => {
    axios.get(`${BACKEND_URL}/user_behavior`)
      .then(res => {
        const formatted = res.data.map((row, index) => ({
          id: index, // needed for DataGrid
          ...row
        }));
        setRows(formatted);
      })
      .catch(err => console.error(err));
  }, []);

  const columns = [
    { field: 'uuid', headerName: 'User ID', width: 150 },
    { field: 'logs', headerName: '# Logs', width: 100 },
    { field: 'unique_accounts', headerName: '# Accounts', width: 120 },
    { field: 'frauds', headerName: '# Frauds', width: 100 },
    { field: 'fraud_rate', headerName: 'Fraud Rate (%)', width: 130 },
    { field: 'locale', headerName: 'Locale', width: 100 },
    {
      field: 'actions',
      headerName: 'Actions',
      width: 150,
      renderCell: (params) => (
        <button onClick={() => onInvestigate(params.row.uuid)}>
          Investigate
        </button>
      )
    }
  ];

  return (
    <div style={{ height: 400, width: '100%' }}>
      <DataGrid
        rows={rows}
        columns={columns}
        pageSize={10}
        rowsPerPageOptions={[10]}
        pagination
        filterModel={{
          items: [],
        }}
      />
    </div>
  );
};

export default UserBehaviorTable;

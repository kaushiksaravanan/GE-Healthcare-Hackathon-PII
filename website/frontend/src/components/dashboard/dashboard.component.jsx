import React, {
  useState,
  useRef,
  useEffect,
  useMemo,
  useCallback,
} from "react";
import axios from "axios";
import defaultVariables from "../variables/variables";
import "./dashboard.css";
import { useNavigate } from "react-router-dom";
import { AgGridReact } from "ag-grid-react";
import "ag-grid-community/styles/ag-grid.css"; // Core grid CSS, always needed
import "ag-grid-community/styles/ag-theme-alpine.css"; // Optional theme CSS
import { useTranslation } from "react-i18next";

const Dashboard = () => {
  const { t, i18n } = useTranslation();

  const gridRef = useRef();
  const [rowData, setRowData] = useState();

  const [columnDefs, setColumnDefs] = useState([
    { field: "documentId", headerName: "Document ID", filter: true, flex: 1 },
    {
      field: "documentName",
      headerName: "Document Name",
      filter: true,
      flex: 2,
      cellRenderer: LinkCellRenderer,
    },
    {
      field: "dataInput",
      headerName: "Input",
      filter: true,
      flex: 5,
    },
    {
      field: "dataOutput",
      headerName: "Output",
      filter: true,
      flex: 5,
    },
  ]);

  function LinkCellRenderer(props) {
    return (
      <a
        style={{ color: "var(--font-color)" }}
        rel="noopener noreferrer"
        href={
          defaultVariables["frontend-url"] +
          "home/logs/view/" +
          props.data.documentId
        }
      >
        {props.value}
      </a>
    );
  }

  const autoGroupColumnDef = useMemo(() => {
    return {
      headerName: "Group",
      minWidth: 170,
      field: "athlete",
      valueGetter: (params) => {
        if (params.node.group) {
          return params.node.key;
        } else {
          return params.data[params.colDef.field];
        }
      },
      headerCheckboxSelection: true,
      cellRenderer: "agGroupCellRenderer",
      cellRendererParams: {
        checkbox: true,
      },
    };
  }, []);

  const defaultColDef = useMemo(() => {
    return {
      editable: false,
      enableRowGroup: true,
      enablePivot: true,
      enableValue: true,
      sortable: true,
      resizable: true,
      filter: true,
      flex: 1,
      minWidth: 200,
    };
  }, []);

  const onGridReady = useCallback((params) => {
    axios
      .get(
        defaultVariables["backend-url"] +
          "logs/get?userid=" +
          localStorage.getItem("userid")
      )
      .then((res) => {
        setRowData(res.data);
      })
      .catch((err) => {
        console.log(err);
      });
  }, []);

  // Export as CSV
  const onBtnExport = useCallback(() => {
    gridRef.current.api.exportDataAsCsv();
  }, []);

  const onCellClicked = () => {
    alert("Cell is Clicked");
  };

  const navigate = useNavigate();
  const navigateToAddActivity = () => {
    navigate("/home/logs/add");
  };

  return (
    <div
      style={{
        width: "90%",
        height: "100%",
        marginLeft: "5%",
        textAlign: "left",
      }}
    >
      <div className="grid-options-div">
        <button className="button-top" onClick={navigateToAddActivity}>
          Add logs
        </button>

        <button className="button-top" onClick={onBtnExport}>
          Export as CSV
        </button>
      </div>

      <div
        className="ag-theme-alpine"
        style={{
          width: "100%",
          height: "calc(100% - 60px)",
          textAlign: "left",
        }}
      >
        <AgGridReact
          ref={gridRef}
          rowData={rowData}
          columnDefs={columnDefs}
          autoGroupColumnDef={autoGroupColumnDef}
          defaultColDef={defaultColDef}
          suppressRowClickSelection={true}
          groupSelectsChildren={true}
          rowSelection={"multiple"}
          rowGroupPanelShow={"always"}
          pivotPanelShow={"always"}
          pagination={true}
          onGridReady={onGridReady}
          // onCellClicked={onCellClicked}
        ></AgGridReact>
      </div>
    </div>
  );
};

export default Dashboard;

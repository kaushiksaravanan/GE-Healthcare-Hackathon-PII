import React from "react";
import { useEffect, useState } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";
import defaultVariables from "../variables/variables";
import "./view-logs.css";
import { useTranslation } from "react-i18next";
import { Button } from "@mui/material";

const ViewLogs = () => {
  const { t } = useTranslation();

  let { id } = useParams();
  const [documentId, setDocumentId] = useState("");
  const [documentName, setDocumentName] = useState("");
  const [documentSize, setDocumentSize] = useState("");
  const [timestamp, setTimestamp] = useState("");
  const [processedTime, setProcessedTime] = useState("");
  const [dataInput, setDataInput] = useState("");
  const [dataOutput, setDataOutput] = useState("");
  const [highlightText, setHighlightText] = useState("");
  const [keyValuePairData, setKeyValuePairData] = useState("");
  const [detectionType, setDetectionType] = useState("");

  const [resultTextToDisplay, setResultTextToDisplay] = useState("");

  useEffect(() => {
    axios
      .get(defaultVariables["backend-url"] + "logs/view/get?id=" + id)
      .then((res) => {
        setDocumentId(res.data[0].documentId);
        setDocumentName(res.data[0].documentName);
        setDocumentSize(res.data[0].documentSize);
        setTimestamp(res.data[0].timestamp);
        setProcessedTime(res.data[0].processedTime);
        setDataInput(res.data[0].dataInput);
        setDataOutput(res.data[0].dataOutput);
        setHighlightText(res.data[0].highlightText);
        setKeyValuePairData(JSON.parse(res.data[0].replacedValueDict));
        setDetectionType(res.data[0].detectionType);

        setResultTextToDisplay(
          res.data[0].dataOutput
            .replace(/(?:\r\n|\r|\n)/g, "<br>")
            .replace(/\[\[(.*?)\]\]/g, "<b>$1</b>")
        );
      })
      .catch((err) => {
        console.log(err);
      });
  }, []);

  const replaceKeyValuePair = (event) => {
    event.preventDefault();

    const replacedContent = Object.entries(keyValuePairData).reduce(
      (acc, [key, value]) => {
        const regex = new RegExp(key, "g");
        return acc.replace(regex, value);
      },
      highlightText
    );

    console.log(replacedContent);

    setDataOutput(replacedContent);
    setResultTextToDisplay(
      replacedContent
        .replace(/(?:\r\n|\r|\n)/g, "<br>")
        .replace(/\[\[(.*?)\]\]/g, "<b>$1</b>")
    );
  };

  const handleKeyValuePairDataInputChange = (event) => {
    const { name, value } = event.target;
    setKeyValuePairData({ ...keyValuePairData, [name]: value }); // Update specific key-value pair
  };

  const showKeyValueTable = () => {
    return (
      <center>
        <br />
        <br />
        <div className="keyvalue-section">
          <p className="heading-small">PII/PHI Replacements</p>
          <div className="keyvalue-head">
            <div>Key</div>
            <div>Value</div>
          </div>
          {Object.entries(keyValuePairData).map(([key, value]) => (
            <div className="keyvalue-div" key={key}>
              <input
                type="text"
                id={key}
                name={key}
                value={key}
                onChange={handleKeyValuePairDataInputChange}
              />
              <p> = </p>
              <input
                type="text"
                id={`${key}-value`}
                name={key} // Use the same name for both key and value fields
                value={value}
                onChange={handleKeyValuePairDataInputChange}
              />
              <br />
            </div>
          ))}
          <br />
          <Button
            style={{
              float: "center",
              backgroundColor: "#1E90FF",
              borderColor: "#6495ED",
              borderRadius: "50px",
              height: "45px",
              padding: "10px 30px 10px 30px",
              fontSize: "16px",
            }}
            sx={{ textTransform: "none" }}
            type="submit"
            variant="contained"
            color="primary"
            onClick={replaceKeyValuePair}
          >
            Replace values
          </Button>
          <br />
          <br />
        </div>
      </center>
    );
  };

  return (
    <div className="activity-details">
      <p className="heading-medium">{documentName}</p>
      <div className="all-details-div">
        <div className="details-div">
          <p className="details-field"> Document Name: </p>
          <p className="details-value">{documentName}</p>
        </div>
        <div className="details-div">
          <p className="details-field"> Document Size: </p>
          <p className="details-value">{documentSize}</p>
        </div>
        <div className="details-div">
          <p className="details-field"> Timestamp: </p>
          <p className="details-value">{timestamp}</p>
        </div>
        <div className="details-div">
          <p className="details-field"> Processed Time: </p>
          <p className="details-value">{processedTime}</p>
        </div>
        <div className="details-div">
          <p className="details-field"> Input: </p>
          <p className="details-value">{dataInput}</p>
        </div>
        <div className="details-div">
          <p className="details-field"> Output: </p>
          <p
            className="contents"
            id="result_data"
            style={{
              textAlign: "left",
            }}
            dangerouslySetInnerHTML={{ __html: resultTextToDisplay }}
          />
        </div>
        <div className="details-div">
          <p className="details-field"> Detection Type: </p>
          <p className="details-value">{detectionType}</p>
        </div>

        {showKeyValueTable()}
      </div>
    </div>
  );
};

export default ViewLogs;

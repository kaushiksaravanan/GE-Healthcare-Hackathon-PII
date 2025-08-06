import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faList,
  faFile,
  faDownload,
  faArrowCircleDown,
  faBolt,
  faRetweet,
  faBars,
  faSnowflake,
  faCheck,
  faCircle,
  faFastForward,
  faStepForward,
} from "@fortawesome/fontawesome-free-solid";
import {
  TextField,
  Button,
  Alert,
  AlertTitle,
  CircularProgress,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import defaultVariables from "../variables/variables";
import BarPlot from "../charts/BarPlot";
import DonutChart from "../charts/DonutChart";
import PieChart from "../charts/PieChart";
import LineChart from "../charts/LineChart";
import Popup from "./popup/Popup";

const AddLogsForm = () => {
  const { t } = useTranslation();

  const navigate = useNavigate();

  // Popup
  const [isPopupOpen, setIsPopupOpen] = useState(false);

  const togglePopup = () => {
    setIsPopupOpen(!isPopupOpen);
  };

  const [successMessage, setSuccessMessage] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);

  const [showProgressBar, setShowProgressBar] = useState(false);

  const [detectionType, setDetectionType] = useState("highlight");
  const [logUploadType, setLogUploadType] = useState("file");
  const [multiThreading, setMultiThreading] = useState("no");
  const [processorType, setProcessorType] = useState("gpu");
  const [chartType, setChartType] = useState("pie");

  const [dataGetUrl, setDataGetUrl] = useState("");

  const [databaseName, setDatabaseName] = useState("test");
  const [databaseHost, setDatabaseHost] = useState("localhost:3306");
  const [databaseUser, setDatabaseUser] = useState("root");
  const [databasePassword, setDatabasePassword] = useState("");

  const [allSelectedFiles, setAllSelectedFiles] = useState([]);
  const [selectedFile, setSelectedFile] = useState("");
  const [fileContent, setFileContent] = useState("");
  const [fileContentToDisplay, setFileContentToDisplay] = useState("");

  const [resultText, setResultText] = useState("");
  const [highlightText, setHighlightText] = useState("");
  const [entityText, setEntityText] = useState("");
  const [redactText, setRedactText] = useState("");
  const [replaceText, setReplaceText] = useState("");

  const [resultTextToDisplay, setResultTextToDisplay] = useState("");
  const [percentageOfPII, setPercentageOfPII] = useState("");
  const [parentPiiInfoList, setParentPiiInfoList] = useState([]);
  const [totalTimeTaken, setTotalTimeTaken] = useState(0);
  const [keyValuePairData, setKeyValuePairData] = useState(JSON.parse("{}"));

  const [documentName, setDocumentName] = useState("");
  const [documentSize, setDocumentSize] = useState("");
  const [documentTimestamp, setDocumentTimestamp] = useState("");
  const [fileInfo, setFileInfo] = useState({
    numCharacters: 0,
    numWords: 0,
    numLines: 0,
    fileSize: 0,
  });

  const processFiles = () => {};

  // useEffect hook
  useEffect(() => {});

  function getTextSizeInBytes(text) {
    const blob = new Blob([text], { type: "text/plain" });
    return blob.size;
  }

  function formatDateString(inputString) {
    // Parse the input string into a Date object
    const date = new Date(inputString);

    // Array of month names
    const monthNames = [
      "January",
      "February",
      "March",
      "April",
      "May",
      "June",
      "July",
      "August",
      "September",
      "October",
      "November",
      "December",
    ];

    // Extract the day, month, and year from the Date object
    const day = date.getDate();
    const month = monthNames[date.getMonth()];
    const year = date.getFullYear();

    // Return the formatted date string
    return `${day} ${month} ${year}`;
  }

  const changeDatabaseType = (database) => {
    if (database == "ftp") {
      setDatabaseHost("192.168.18.40");
      setDatabaseName("test_file.txt");
      setDatabaseUser("fazil");
      setDatabasePassword("fazil");
    }
    if (database == "database-mysql") {
      setDatabaseHost("localhost:3306");
      setDatabaseName("test");
      setDatabaseUser("root");
      setDatabasePassword("");
    }
    if (database == "database-postgres") {
      setDatabaseHost("localhost:5432");
      setDatabaseName("test");
      setDatabaseUser("postgres");
      setDatabasePassword("fazil");
    }
    if (database == "database-sqlite") {
      setDatabaseHost(
        "D:/Hackathons/GE Healthcare/GE-Healthcare-Hackathon/testing/database_dumb_dir"
      );
      setDatabaseName("test.db");
      setDatabaseUser("");
      setDatabasePassword("");
    }
    setLogUploadType(database);
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (logUploadType == "file") {
      const formData = new FormData();
      formData.append("myFile", selectedFile, selectedFile.name);
      console.log(selectedFile);
    }

    // Request Data
    const request_data = {
      detection_type: detectionType,
      logs_content: fileContent,
      document_name: documentName,
      document_size: documentSize,
      document_timestamp: documentTimestamp,
      multithreading: multiThreading,
      processor_type: processorType,
    };

    // Enable the progress bar.
    setShowProgressBar(true);

    axios
      .post(defaultVariables["backend-url"] + "logs/add", request_data)
      .then((res) => {
        setTimeout(() => {
          setSuccessMessage(null);
          setShowProgressBar(false);
          setResultText(res.data.replace_text);
          setHighlightText(res.data.highlighted_text);
          setEntityText(res.data.entity_text);
          setRedactText(res.data.redact_text);
          setReplaceText(res.data.replace_text);
          // setResultTextToDisplay(
          //   res.data.text
          //     .replace(/(?:\r\n|\r|\n)/g, "<br>")
          //     .replace(/\[\[(.*?)\]\]/g, "<b>$1</b>")
          // );
          setPercentageOfPII(res.data.percentage_of_pii);
          setParentPiiInfoList(res.data.parent_pii_info_list);
          setTotalTimeTaken(res.data.total_time_taken);
          const jsonString = JSON.stringify(res.data.replaced_value_dict);
          console.log(jsonString);
          setKeyValuePairData(JSON.parse(jsonString));

          if (detectionType == "redact") {
            setResultText(res.data.redact_text);
            setResultTextToDisplay(
              res.data.redact_text
                .replace(/(?:\r\n|\r|\n)/g, "<br>")
                .replace(/\[\[(.*?)\]\]/g, "<b>$1</b>")
            );
          }
          if (detectionType == "replace") {
            setResultText(res.data.replace_text);
            setResultTextToDisplay(
              res.data.replace_text
                .replace(/(?:\r\n|\r|\n)/g, "<br>")
                .replace(/\[\[(.*?)\]\]/g, "<b>$1</b>")
            );
          }
          if (detectionType == "entity") {
            setResultText(res.data.entity_text);
            setResultTextToDisplay(
              res.data.entity_text
                .replace(/(?:\r\n|\r|\n)/g, "<br>")
                .replace(/\[\[(.*?)\]\]/g, "<b>$1</b>")
            );
          }
          if (detectionType == "highlight") {
            setResultText(res.data.highlighted_text);
            setResultTextToDisplay(
              res.data.highlighted_text
                .replace(/(?:\r\n|\r|\n)/g, "<br>")
                .replace(/\[\[(.*?)\]\]/g, "<b>$1</b>")
            );
          }

          // setExactResultText(detectionType);
          // navigate("/home/grievance/select/" + res.data.grievance_id);
        }, 3000);
      })
      .catch((err) => {
        setShowProgressBar(false);
        setErrorMessage("Some error occured");
        setTimeout(() => {
          setErrorMessage(null);
        }, 3000);
      });
  };

  const saveToDatabase = (e) => {
    e.preventDefault();

    // Request Data
    const request_data = {
      detection_type: detectionType,
      input: fileContent,
      document_name: documentName,
      document_size: documentSize,
      document_timestamp: documentTimestamp,
      total_time_taken: totalTimeTaken,
      output: resultText,
      highlight_text: highlightText,
      replaced_value_dict: JSON.stringify(keyValuePairData),
    };

    // Enable the progress bar.
    setShowProgressBar(true);

    axios
      .post(defaultVariables["backend-url"] + "logs/save", request_data)
      .then((res) => {
        setTimeout(() => {
          setSuccessMessage(null);
          setShowProgressBar(false);
          navigate("/home/dashboard");
        }, 3000);
      })
      .catch((err) => {
        setShowProgressBar(false);
        setErrorMessage("Some error occured");
        setTimeout(() => {
          setErrorMessage(null);
        }, 3000);
      });
  };

  const changeDetectionType = (detection_type) => {
    setDetectionType(detection_type);
    setExactResultText(detection_type);
  };

  const setExactResultText = (detection_type) => {
    console.log("Inside function setExactResultText");
    console.log(detection_type);
    if (detection_type == "redact") {
      setResultText(redactText);

      setResultTextToDisplay(
        redactText
          .replace(/(?:\r\n|\r|\n)/g, "<br>")
          .replace(/\[\[(.*?)\]\]/g, "<b>$1</b>")
      );
    }
    if (detection_type == "replace") {
      setResultText(replaceText);

      setResultTextToDisplay(
        replaceText
          .replace(/(?:\r\n|\r|\n)/g, "<br>")
          .replace(/\[\[(.*?)\]\]/g, "<b>$1</b>")
      );
    }
    if (detection_type == "entity") {
      setResultText(entityText);

      setResultTextToDisplay(
        entityText
          .replace(/(?:\r\n|\r|\n)/g, "<br>")
          .replace(/\[\[(.*?)\]\]/g, "<b>$1</b>")
      );
    }
    if (detection_type == "highlight") {
      setResultText(highlightText);

      setResultTextToDisplay(
        highlightText
          .replace(/(?:\r\n|\r|\n)/g, "<br>")
          .replace(/\[\[(.*?)\]\]/g, "<b>$1</b>")
      );
    }
  };

  // Create a reference to the hidden file input element
  const hiddenFileInput = useRef(null);

  // Programatically click the hidden file input element
  // when the Button component is clicked
  const handleClick = (event) => {
    hiddenFileInput.current.click();
  };

  const handleTextChange = (event) => {
    let content = event.target.value;
    let numCharacters = content.length;
    let numWords = content.split(/\s+/).filter(Boolean).length;
    let numLines = content.split(/\n/).length;
    let fileSize = getTextSizeInBytes(content);
    setFileContent(content);
    setFileInfo({
      numCharacters,
      numWords,
      numLines,
      fileSize,
    });
  };

  // Call a function (passed as a prop from the parent component)
  // to handle the user-selected file
  const handleFileChange = (event) => {
    // Upload multiple files.
    const chosenFiles = Array.prototype.slice.call(event.target.files);
    setAllSelectedFiles(chosenFiles);

    let concatenatedFileContents = "";
    let concatenatedFileContentsToDisplay = "";

    let numCharacters = 0;
    let numWords = 0;
    let numLines = 0;
    let fileSize = 0;

    chosenFiles.map((individualFile) => {
      const fileReader = new FileReader();
      fileReader.readAsText(individualFile, "UTF-8");
      fileReader.onload = (e) => {
        const content = e.target.result;
        if (concatenatedFileContents != "") {
          concatenatedFileContents += "\n" + content;
        } else {
          concatenatedFileContents = content;
        }

        // If it is JSON, then use JSON.parse(content);
        setFileContent(concatenatedFileContents);
        // For display purpose
        concatenatedFileContentsToDisplay = concatenatedFileContents.replace(
          /(?:\r\n|\r|\n)/g,
          "<br>"
        );
        setFileContentToDisplay(concatenatedFileContentsToDisplay);

        numCharacters += content.length;
        numWords += content.split(/\s+/).filter(Boolean).length;
        numLines += content.split(/\n/).length;
        // fileSize += content.size;
        fileSize = getTextSizeInBytes(concatenatedFileContents);

        setFileInfo({
          numCharacters,
          numWords,
          numLines,
          fileSize,
        });
      };
    });

    // Upload single file.
    const fileUploaded = event.target.files[0];
    setSelectedFile(fileUploaded);
    setDocumentName(fileUploaded.name);
    setDocumentSize(fileUploaded.size);
    setDocumentTimestamp(fileUploaded.lastModified);
    // console.log("DEBUG:");
    // console.log("File Details");
    // console.log(fileUploaded.name);
    // console.log(fileUploaded.size);
    // console.log(fileUploaded.lastModified);
  };

  const downloadResult = (event) => {
    const element = document.createElement("a");
    // const file = new Blob([document.getElementById("result_data").innerHTML], {
    //   type: "text/plain",
    // });
    const file = new Blob([resultText], {
      type: "text/plain",
    });
    element.href = URL.createObjectURL(file);
    element.download = "logs.txt";
    document.body.appendChild(element); // Required for this to work in FireFox
    element.click();
  };

  const contentDetails = () => {
    return (
      <center>
        <div className="div-data">
          <p className="title">Content Details:</p>
          <table>
            <tr>
              <td>Number of characters:</td>
              <td>
                <b>{fileInfo.numCharacters}</b>
              </td>
            </tr>

            <tr>
              <td>Number of words:</td>
              <td>
                <b>{fileInfo.numWords}</b>
              </td>
            </tr>

            <tr>
              <td>Number of lines:</td>
              <td>
                <b>{fileInfo.numLines}</b>
              </td>
            </tr>

            <tr>
              <td>Total Size:</td>
              <td>
                <b>{fileInfo.fileSize} bytes</b>
              </td>
            </tr>
          </table>
        </div>
      </center>
    );
  };

  const selectedFileNames = () => {
    if (selectedFile) {
      return (
        <center>
          <div className="div-data">
            <p className="title">Selected Files:</p>
            <table>
              <tr>
                <th className="col1">Name</th>
                <th>Size</th>
                <th>Type</th>
                <th>Last Modified</th>
              </tr>
              {allSelectedFiles.map((individualFile) => {
                return (
                  <tr className="row">
                    <td className="file-name col1">{individualFile.name}</td>
                    <td>{individualFile.size}</td>
                    <td>{individualFile.type}</td>
                    <td>
                      {formatDateString(
                        individualFile.lastModifiedDate.toLocaleDateString()
                      )}
                    </td>
                  </tr>
                );
              })}
            </table>
          </div>
        </center>
      );
    } else {
      return (
        <div>
          <br />
          <h4>Please upload a file before submitting.</h4>
        </div>
      );
    }
  };

  const fileData = () => {
    if (selectedFile) {
      return (
        <center>
          <div className="div-data">
            {/* <p>
            <b>File Details:</b>
          </p>
          <p>File Name: {selectedFile.name}</p>
          <p>File Type: {selectedFile.type}</p>
          <p>Last Modified: {selectedFile.lastModifiedDate.toDateString()}</p>
          <p>File Contents: {fileContent}</p> */}
            <p className="title">Log contents:</p>
            <p
              style={{
                maxHeight: "500px",
                overflow: "scroll",
              }}
              className="contents"
              contentEditable
              dangerouslySetInnerHTML={{ __html: fileContentToDisplay }}
            />
          </div>
        </center>
      );
    } else {
      return <div></div>;
    }
  };

  const resultData = () => {
    if (resultText) {
      return (
        <center>
          <div className="div-data">
            <div style={{ display: "flex" }}>
              <p className="title" style={{ width: "100%" }}>
                Result:
              </p>
              <p
                style={{
                  lineHeight: "35px",
                  width: "500px",
                  color: "dodgerblue",
                  fontWeight: "bold",
                  fontSize: "14px",
                }}
              >
                Percentage of PII: {percentageOfPII} %
              </p>
              <p
                style={{
                  lineHeight: "35px",
                  width: "300px",
                  color: "dodgerblue",
                  fontWeight: "bold",
                  fontSize: "14px",
                }}
              >
                Time: {totalTimeTaken} s
              </p>
              <Button
                style={{
                  float: "center",
                  backgroundColor: "#1E90FF",
                  borderColor: "#6495ED",
                  borderRadius: "50px",
                  height: "35px",
                  padding: "10px 30px 10px 30px",
                  fontSize: "14px",
                }}
                sx={{ textTransform: "none" }}
                variant="contained"
                color="primary"
                onClick={downloadResult}
              >
                <FontAwesomeIcon icon={faDownload} /> &nbsp;&nbsp;Download
              </Button>
            </div>

            <p
              className="contents"
              id="result_data"
              dangerouslySetInnerHTML={{ __html: resultTextToDisplay }}
            />
          </div>
        </center>
      );
    } else {
      return (
        <div>
          <br />
          <h4>No results.</h4>
        </div>
      );
    }
  };

  const generatePieChart = () => {
    if (resultText) {
      return (
        <div>
          <br />
          <br />

          <div className="options-div">
            <div
              className="option-categories"
              style={{
                background:
                  "linear-gradient( 135deg, #FEB692 10%, #EA5455 100%)",
              }}
            >
              <p className="option-title">Chart Type</p>
              <br />

              <div
                className="option-category"
                onClick={() => {
                  setChartType("bar");
                }}
                style={{
                  backgroundColor: chartType == "bar" ? "lightblue" : "white",
                  fontWeight: chartType == "bar" ? "bold" : "normal",
                  cursor: "pointer",
                }}
              >
                <p>
                  {<FontAwesomeIcon icon={faBolt} />}
                  &nbsp;&nbsp; Bar
                </p>
              </div>
              <div
                className="option-category"
                onClick={() => {
                  setChartType("donut");
                }}
                style={{
                  backgroundColor: chartType == "donut" ? "lightblue" : "white",
                  fontWeight: chartType == "donut" ? "bold" : "normal",
                  cursor: "pointer",
                }}
              >
                <p>
                  {<FontAwesomeIcon icon={faBolt} />}
                  &nbsp;&nbsp; Donut
                </p>
              </div>
              <div
                className="option-category"
                onClick={() => {
                  setChartType("line");
                }}
                style={{
                  backgroundColor: chartType == "line" ? "lightblue" : "white",
                  fontWeight: chartType == "line" ? "bold" : "normal",
                  cursor: "pointer",
                }}
              >
                <p>
                  {<FontAwesomeIcon icon={faBolt} />}
                  &nbsp;&nbsp; Line
                </p>
              </div>
              <div
                className="option-category"
                onClick={() => {
                  setChartType("pie");
                }}
                style={{
                  backgroundColor: chartType == "pie" ? "lightblue" : "white",
                  fontWeight: chartType == "pie" ? "bold" : "normal",
                  cursor: "pointer",
                }}
              >
                <p>
                  {<FontAwesomeIcon icon={faBolt} />}
                  &nbsp;&nbsp; Pie
                </p>
              </div>
            </div>
          </div>
          <br />
          <center>
            <h4>PII Types</h4>
            <div className="chart-div">
              {chartType == "pie" && (
                <PieChart
                  data={parentPiiInfoList[1]}
                  labels={parentPiiInfoList[0]}
                />
              )}
              {chartType == "donut" && (
                <DonutChart
                  data={parentPiiInfoList[1]}
                  labels={parentPiiInfoList[0]}
                />
              )}
              {chartType == "line" && (
                <LineChart
                  ytitle="PII Types"
                  data={parentPiiInfoList[1]}
                  labels={parentPiiInfoList[0]}
                />
              )}
              {chartType == "bar" && (
                <BarPlot
                  options={{ horizontal: false }}
                  data={parentPiiInfoList[1]}
                  labels={parentPiiInfoList[0]}
                  ylabel={"PII Types"}
                />
              )}
            </div>
          </center>
        </div>
      );
    }
  };

  const getContents = (event) => {
    event.preventDefault();

    // Request Data
    const request_data = {
      data_get_type: logUploadType,
      data_get_url: dataGetUrl,
      database_host: databaseHost,
      database_name: databaseName,
      database_user: databaseUser,
      database_password: databasePassword,
    };

    // Enable the progress bar.
    setShowProgressBar(true);

    axios
      .post(defaultVariables["backend-url"] + "logs/getcontents", request_data)
      .then((res) => {
        setTimeout(() => {
          setSuccessMessage(null);
          setShowProgressBar(false);
          setFileContent(res.data.response);
        }, 3000);
      })
      .catch((err) => {
        setShowProgressBar(false);
        setErrorMessage("Some error occured");
        setTimeout(() => {
          setErrorMessage(null);
        }, 3000);
      });
  };

  const showDatabaseInfoForm = () => {
    return (
      <>
        <br />
        <br />
        <p className="heading-small">Database Credentials</p>
        <br />
        <br />
        <TextField
          style={{
            width: "80%",
            backgroundColor: "white",
          }}
          label={"Database Host"}
          variant="outlined"
          value={databaseHost}
          onChange={(e) => {
            setDatabaseHost(e.target.value);
          }}
          fullWidth
          margin="normal"
        />
        <br />
        <br />
        <TextField
          style={{
            width: "80%",
            backgroundColor: "white",
          }}
          label={"Database Name"}
          variant="outlined"
          value={databaseName}
          onChange={(e) => {
            setDatabaseName(e.target.value);
          }}
          fullWidth
          margin="normal"
        />
        <br />
        <br />
        <TextField
          style={{
            width: "80%",
            backgroundColor: "white",
          }}
          label={"Database User"}
          variant="outlined"
          value={databaseUser}
          onChange={(e) => {
            setDatabaseUser(e.target.value);
          }}
          fullWidth
          margin="normal"
        />
        <br />
        <br />
        <TextField
          style={{
            width: "80%",
            backgroundColor: "white",
          }}
          label={"Database Password"}
          variant="outlined"
          value={databasePassword}
          onChange={(e) => {
            setDatabasePassword(e.target.value);
          }}
          fullWidth
          margin="normal"
        />
        <br />
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
          onClick={getContents}
        >
          Connect to DB and get data
        </Button>
        <br />
        <br />
      </>
    );
  };

  const showFTPInfoForm = () => {
    return (
      <>
        <br />
        <br />
        <p className="heading-small">FTP Credentials</p>
        <br />
        <br />
        <TextField
          style={{
            width: "80%",
            backgroundColor: "white",
          }}
          label={"FTP Host"}
          variant="outlined"
          value={databaseHost}
          onChange={(e) => {
            setDatabaseHost(e.target.value);
          }}
          fullWidth
          margin="normal"
        />
        <br />
        <br />
        <TextField
          style={{
            width: "80%",
            backgroundColor: "white",
          }}
          label={"FTP User"}
          variant="outlined"
          value={databaseUser}
          onChange={(e) => {
            setDatabaseUser(e.target.value);
          }}
          fullWidth
          margin="normal"
        />
        <br />
        <br />
        <TextField
          style={{
            width: "80%",
            backgroundColor: "white",
          }}
          label={"FTP Password"}
          variant="outlined"
          value={databasePassword}
          onChange={(e) => {
            setDatabasePassword(e.target.value);
          }}
          fullWidth
          margin="normal"
        />
        <br />
        <br />
        <TextField
          style={{
            width: "80%",
            backgroundColor: "white",
          }}
          label={"File Path"}
          variant="outlined"
          value={databaseName}
          onChange={(e) => {
            setDatabaseName(e.target.value);
          }}
          fullWidth
          margin="normal"
        />
        <br />
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
          onClick={getContents}
        >
          Connect to FTP and load file
        </Button>
        <br />
        <br />
      </>
    );
  };

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

    setReplaceText(replacedContent);
    setResultText(replacedContent);
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
    <div>
      <div className="form-div">
        <br />

        <p
          className="heading-small"
          style={{ textAlign: "left", color: "black" }}
        >
          {<FontAwesomeIcon icon={faSnowflake} />}&nbsp;&nbsp;Upload Logs
        </p>

        <br />

        <div className="options-div">
          <div
            className="option-categories"
            style={{
              background: "linear-gradient( 135deg, #FEB692 10%, #EA5455 100%)",
            }}
          >
            <p className="option-title">Redaction type</p>
            <br />

            <div
              className="option-category"
              onClick={() => {
                changeDetectionType("highlight");
              }}
              style={{
                backgroundColor:
                  detectionType == "highlight" ? "lightblue" : "white",
                fontWeight: detectionType == "highlight" ? "bold" : "normal",
                cursor: "pointer",
              }}
            >
              <p>
                {<FontAwesomeIcon icon={faRetweet} />}
                &nbsp;&nbsp; Highlight
              </p>
            </div>
            <div
              className="option-category"
              onClick={() => {
                changeDetectionType("entity");
              }}
              style={{
                backgroundColor:
                  detectionType == "entity" ? "lightblue" : "white",
                fontWeight: detectionType == "entity" ? "bold" : "normal",
                cursor: "pointer",
              }}
            >
              <p>
                {<FontAwesomeIcon icon={faRetweet} />}
                &nbsp;&nbsp; Entity
              </p>
            </div>
            <div
              className="option-category"
              onClick={() => {
                changeDetectionType("redact");
              }}
              style={{
                backgroundColor:
                  detectionType == "redact" ? "lightblue" : "white",
                fontWeight: detectionType == "redact" ? "bold" : "normal",
                cursor: "pointer",
              }}
            >
              <p>
                {<FontAwesomeIcon icon={faBolt} />}
                &nbsp;&nbsp; Redact
              </p>
            </div>
            <div
              className="option-category"
              onClick={() => {
                changeDetectionType("replace");
              }}
              style={{
                backgroundColor:
                  detectionType == "replace" ? "lightblue" : "white",
                fontWeight: detectionType == "replace" ? "bold" : "normal",
                cursor: "pointer",
              }}
            >
              <p>
                {<FontAwesomeIcon icon={faRetweet} />}
                &nbsp;&nbsp; Replace
              </p>
            </div>
          </div>

          <div
            className="option-categories"
            style={{
              background: "linear-gradient( 135deg, #FDEB71 10%, #F8D800 100%)",
            }}
          >
            <p className="option-title">Processor</p>
            <br />

            <div
              className="option-category"
              onClick={() => {
                setProcessorType("cpu");
              }}
              style={{
                backgroundColor:
                  processorType == "cpu" ? "lightskyblue" : "white",
                fontWeight: processorType == "cpu" ? "bold" : "normal",
                cursor: "pointer",
              }}
            >
              <p>
                {<FontAwesomeIcon icon={faStepForward} />}
                &nbsp;&nbsp; CPU
              </p>
            </div>
            <div
              className="option-category"
              onClick={() => {
                setProcessorType("gpu");
              }}
              style={{
                backgroundColor:
                  processorType == "gpu" ? "lightskyblue" : "white",
                fontWeight: processorType == "gpu" ? "bold" : "normal",
                cursor: "pointer",
              }}
            >
              <p>
                {<FontAwesomeIcon icon={faFastForward} />}
                &nbsp;&nbsp; GPU
              </p>
            </div>
          </div>
        </div>

        <div className="options-div">
          <div
            className="option-categories"
            style={{
              background: "linear-gradient( 135deg, #F761A1 10%, #c93eef 100%)",
            }}
          >
            <p className="option-title">Source</p>
            <br />

            <div
              className="option-category"
              onClick={() => {
                setLogUploadType("file");
              }}
              style={{
                backgroundColor:
                  logUploadType == "file" ? "lightskyblue" : "white",
                fontWeight: logUploadType == "file" ? "bold" : "normal",
                cursor: "pointer",
              }}
            >
              <p>
                {<FontAwesomeIcon icon={faFile} />}
                &nbsp;&nbsp; File Upload
              </p>
            </div>
            <div
              className="option-category"
              onClick={() => {
                setLogUploadType("text");
              }}
              style={{
                backgroundColor:
                  logUploadType == "text" ? "lightskyblue" : "white",
                fontWeight: logUploadType == "text" ? "bold" : "normal",
                cursor: "pointer",
              }}
            >
              <p>
                {<FontAwesomeIcon icon={faList} />}
                &nbsp;&nbsp; Text
              </p>
            </div>
            <div
              className="option-category"
              onClick={() => {
                setLogUploadType("url-html");
              }}
              style={{
                backgroundColor:
                  logUploadType == "url-html" ? "lightskyblue" : "white",
                fontWeight: logUploadType == "url-html" ? "bold" : "normal",
                cursor: "pointer",
              }}
            >
              <p>
                {<FontAwesomeIcon icon={faFile} />}
                &nbsp;&nbsp; URL (html)
              </p>
            </div>
            <div
              className="option-category"
              onClick={() => {
                setLogUploadType("url-contents");
              }}
              style={{
                backgroundColor:
                  logUploadType == "url-contents" ? "lightskyblue" : "white",
                fontWeight: logUploadType == "url-contents" ? "bold" : "normal",
                cursor: "pointer",
              }}
            >
              <p>
                {<FontAwesomeIcon icon={faFile} />}
                &nbsp;&nbsp; URL (contents)
              </p>
            </div>
            <div
              className="option-category"
              onClick={() => {
                changeDatabaseType("ftp");
              }}
              style={{
                backgroundColor:
                  logUploadType == "ftp" ? "lightskyblue" : "white",
                fontWeight: logUploadType == "ftp" ? "bold" : "normal",
                cursor: "pointer",
              }}
            >
              <p>
                {<FontAwesomeIcon icon={faFile} />}
                &nbsp;&nbsp; FTP
              </p>
            </div>
            <div
              className="option-category"
              onClick={() => {
                changeDatabaseType("file-location");
              }}
              style={{
                backgroundColor:
                  logUploadType == "file-location" ? "lightskyblue" : "white",
                fontWeight:
                  logUploadType == "file-location" ? "bold" : "normal",
                cursor: "pointer",
              }}
            >
              <p>
                {<FontAwesomeIcon icon={faFile} />}
                &nbsp;&nbsp; Directory Load
              </p>
            </div>
            <div
              className="option-category"
              onClick={() => {
                changeDatabaseType("database-mysql");
              }}
              style={{
                backgroundColor:
                  logUploadType == "database-mysql" ? "lightskyblue" : "white",
                fontWeight:
                  logUploadType == "database-mysql" ? "bold" : "normal",
                cursor: "pointer",
              }}
            >
              <p>
                {<FontAwesomeIcon icon={faFile} />}
                &nbsp;&nbsp; Database (MySQL)
              </p>
            </div>
            <div
              className="option-category"
              onClick={() => {
                changeDatabaseType("database-postgres");
              }}
              style={{
                backgroundColor:
                  logUploadType == "database-postgres"
                    ? "lightskyblue"
                    : "white",
                fontWeight:
                  logUploadType == "database-postgres" ? "bold" : "normal",
                cursor: "pointer",
              }}
            >
              <p>
                {<FontAwesomeIcon icon={faFile} />}
                &nbsp;&nbsp; Database (Postgres)
              </p>
            </div>
            <div
              className="option-category"
              onClick={() => {
                changeDatabaseType("database-sqlite");
              }}
              style={{
                backgroundColor:
                  logUploadType == "database-sqlite" ? "lightskyblue" : "white",
                fontWeight:
                  logUploadType == "database-sqlite" ? "bold" : "normal",
                cursor: "pointer",
              }}
            >
              <p>
                {<FontAwesomeIcon icon={faFile} />}
                &nbsp;&nbsp; Database (SQLite)
              </p>
            </div>
          </div>

          <div
            className="option-categories"
            style={{
              display: "none",
              background: "linear-gradient( 135deg, #81FBB8 10%, #28C76F 100%)",
            }}
          >
            <p className="option-title">Multi-processing</p>
            <br />

            <div
              className="option-category"
              onClick={() => {
                setMultiThreading("yes");
              }}
              style={{
                backgroundColor:
                  multiThreading == "yes" ? "lightblue" : "white",
                fontWeight: multiThreading == "yes" ? "bold" : "normal",
                cursor: "pointer",
              }}
            >
              <p>
                {<FontAwesomeIcon icon={faCheck} />}
                &nbsp;&nbsp; Yes
              </p>
            </div>
            <div
              className="option-category"
              onClick={() => {
                setMultiThreading("no");
              }}
              style={{
                backgroundColor: multiThreading == "no" ? "lightblue" : "white",
                fontWeight: multiThreading == "no" ? "bold" : "normal",
                cursor: "pointer",
              }}
            >
              <p>
                {<FontAwesomeIcon icon={faCircle} />}
                &nbsp;&nbsp; No
              </p>
            </div>
          </div>
        </div>

        {logUploadType == "file" && (
          <>
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
              onClick={handleClick}
            >
              Upload Log Files
            </Button>
            <input
              type="file"
              multiple
              onChange={handleFileChange}
              ref={hiddenFileInput}
              style={{ display: "none" }}
            />
          </>
        )}

        {(logUploadType == "url-html" ||
          logUploadType == "url-contents" ||
          logUploadType == "file-location") && (
          <>
            <TextField
              style={{
                width: "80%",
                backgroundColor: "white",
              }}
              label={"Enter the URL or Location."}
              variant="outlined"
              value={dataGetUrl}
              onChange={(e) => {
                setDataGetUrl(e.target.value);
              }}
              fullWidth
              margin="normal"
              required
            />
            <br />
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
              onClick={getContents}
            >
              Get Contents
            </Button>
            <br />
            <br />
          </>
        )}

        {(logUploadType == "database-mysql" ||
          logUploadType == "database-postgres" ||
          logUploadType == "database-sqlite") &&
          showDatabaseInfoForm()}

        {logUploadType == "ftp" && showFTPInfoForm()}

        <form onSubmit={handleSubmit}>
          {(logUploadType == "text" ||
            logUploadType == "url-html" ||
            logUploadType == "url-contents" ||
            logUploadType == "ftp" ||
            logUploadType == "file-location" ||
            logUploadType == "database-mysql" ||
            logUploadType == "database-postgres" ||
            logUploadType == "database-sqlite") && (
            <>
              <TextField
                style={{
                  width: "80%",
                  backgroundColor: "white",
                }}
                label={"Enter the contents of the log."}
                variant="outlined"
                value={fileContent}
                onChange={handleTextChange}
                fullWidth
                multiline
                rows={6}
                margin="normal"
                required
              />
            </>
          )}

          {logUploadType == "file" && fileData()}
          {logUploadType == "file" && selectedFileNames()}
          {contentDetails()}
          {showProgressBar && (
            <div>
              <br />
              <br />
              <CircularProgress />
              <br />
              <br />
            </div>
          )}

          <br />
          <br />
          <Button
            style={{
              width: "30%",
            }}
            type="submit"
            variant="contained"
            color="primary"
            id="react-button"
          >
            {t("submit")}
          </Button>
          <br />
          <br />

          {resultText && resultData()}
          {resultText && detectionType == "replace" && showKeyValueTable()}
          {resultText && generatePieChart()}
        </form>

        {resultText && (
          <>
            <br />
            <br />
            <Button
              onClick={togglePopup}
              style={{
                float: "center",
                backgroundColor: "#1E90FF",
                borderColor: "#6495ED",
                height: "45px",
                width: "30%",
                padding: "10px 30px 10px 30px",
                fontSize: "16px",
                fontWeight: "bold",
              }}
              sx={{ textTransform: "none" }}
              type="submit"
              variant="contained"
              color="primary"
            >
              Save
            </Button>
          </>
        )}

        <Popup show={isPopupOpen} handleClose={togglePopup}>
          <p className="heading-small">Save contents</p>
          <p>Do you want to save the input and output.</p>
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
            onClick={saveToDatabase}
          >
            Save
          </Button>
        </Popup>
      </div>

      {successMessage && (
        <div
          style={{
            position: "fixed",
            top: "60px",
            right: "20px",
            zIndex: 9999,
          }}
        >
          <Alert
            severity="success"
            onClose={() => setSuccessMessage(null)}
            variant="standard"
          >
            <AlertTitle>Success</AlertTitle>
            <strong>{successMessage}</strong>
          </Alert>
        </div>
      )}
      {errorMessage && (
        <div
          style={{
            position: "fixed",
            top: "60px",
            right: "20px",
            zIndex: 9999,
          }}
        >
          <Alert
            severity="error"
            onClose={() => setErrorMessage(null)}
            variant="standard"
            width={{ sx: 300 }}
          >
            <AlertTitle>Error</AlertTitle>
            <strong>{errorMessage}</strong>
          </Alert>
        </div>
      )}
    </div>
  );
};

export default AddLogsForm;

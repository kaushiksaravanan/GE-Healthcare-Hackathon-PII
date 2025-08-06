import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import avatarProfileIcon from "../assets/avatar_profile_icon.png";
import passwordIcon from "../assets/password_icon.png";
import axios from "axios";
import defaultVariables from "./variables/variables";
import { useTranslation } from "react-i18next";
import LanguageSelector from "./language-selector";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faUser } from "@fortawesome/fontawesome-free-solid";
import {
  TextField,
  Button,
  Alert,
  AlertTitle,
  CircularProgress,
} from "@mui/material";

const Login = (props) => {
  const { t } = useTranslation();

  const navigate = useNavigate();

  const [errorMessage, setErrorMessage] = useState(null);

  const [noOfFiles, setNoOfFiles] = useState(0);
  const [noOfWords, setNoOfWords] = useState(0);
  const [noOfPII, setNoOfPII] = useState(0);
  const [noOfTime, setNoOfTime] = useState(0);

  // Update the application statistics
  useEffect(() => {
    axios
      .get(defaultVariables["backend-url"] + "application/statistics")
      .then((result) => {
        setNoOfFiles(result.data.no_of_files);
        setNoOfWords(result.data.no_of_words);
        setNoOfPII(result.data.no_of_pii);
        setNoOfTime(result.data.no_of_time);
      })
      .catch((err) => {
        console.log(err);
      });
  }, []);

  function userLogin(event) {
    event.preventDefault();
    let username = event.target[0].value;
    let password = event.target[1].value;
    const parameters = { username: username, password: password, role: "user" };

    axios
      .post(defaultVariables["backend-url"] + "login", parameters)
      .then((response) => {
        props.setIsAuthenticated(true);
        if (response.data.auth == "success") {
          localStorage.setItem("userid", response.data.userid);
          navigate("/home/logs/add");
        } else {
          setErrorMessage("Login failed");
          setTimeout(() => {
            setErrorMessage(null);
          }, 3000);
        }
      })
      .catch((error) => {
        alert(error);
      });
  }

  function guestLogin() {
    props.setIsAuthenticated(true);
    localStorage.setItem("userid", "0");
    navigate("/home/logs/add");
  }

  return (
    <div>
      <section class="sticky">
        <div class="bubbles">
          <div class="bubble"></div>
          <div class="bubble"></div>
          <div class="bubble"></div>
          <div class="bubble"></div>
          <div class="bubble"></div>
          <div class="bubble"></div>
          <div class="bubble"></div>
          <div class="bubble"></div>
          <div class="bubble"></div>
          <div class="bubble"></div>
        </div>
      </section>
      <div className="login-container">
        <div className="login-container-left">
          <div
            style={{
              zIndex: "2",
              background:
                "linear-gradient(45deg, #ff9a9e 0%, #fad0c4 99%, #fad0c4 100%)",
            }}
          >
            <p className="heading-small">Number of files processed</p>
            <p className="heading-large">{noOfFiles}</p>
          </div>
          <div
            style={{
              zIndex: "2",
              background: "linear-gradient(to top, #fbc2eb 0%, #a6c1ee 100%)",
            }}
          >
            <p className="heading-small">Number of words processed</p>
            <p className="heading-large">{noOfWords}</p>
          </div>
        </div>

        <div style={{ zIndex: "2" }}>
          <center>
            <div className="login-form">
              <form onSubmit={userLogin}>
                <p className="heading-medium" style={{ textAlign: "left" }}>
                  logsPII - Silverine Arts
                </p>
                <br />

                <p
                  className="heading-small"
                  style={{ textAlign: "left", color: "black" }}
                >
                  Login
                </p>
                <br />

                <div className="box">
                  <img src={avatarProfileIcon} />
                  <input type="text" placeholder="Email" />
                </div>

                <div className="box">
                  <img src={passwordIcon} />
                  <input type="password" placeholder={t("password")} />
                </div>

                <button className="form-button">{t("login")}</button>
              </form>
              <button
                style={{ background: "dodgerblue", borderColor: "dodgerblue" }}
                onClick={guestLogin}
                className="form-button"
              >
                Login as Guest
              </button>
            </div>
          </center>
        </div>

        <div className="login-container-right">
          <div
            style={{
              zIndex: "2",
              background: "linear-gradient(120deg, #d4fc79 0%, #96e6a1 100%)",
            }}
          >
            <p className="heading-small">Number of PIIs detected</p>
            <p className="heading-large">{noOfPII}</p>
          </div>
          <div
            style={{
              zIndex: "2",
              background: "linear-gradient(to top, #fff1eb 0%, #ace0f9 100%)",
            }}
          >
            <p className="heading-small">Time taken to process 100 words</p>
            <p className="heading-large">{noOfTime} s</p>
          </div>
        </div>
      </div>
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

export default Login;

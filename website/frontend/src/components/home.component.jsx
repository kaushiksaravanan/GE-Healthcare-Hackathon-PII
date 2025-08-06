import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

import Header from "./header";
import Footer from "./footer";
import SideBar from "./sidebar";
import Dashboard from "./dashboard/dashboard.component";
import AddPeopleForm from "./people/form.component";
import AddLogsForm from "./logs-contents/add-logs.component";
import SelectGrievance from "./logs-contents/select-grievance.component";
import ViewLogs from "./dashboard/view-logs.component";

const Home = () => {
  const navigate = useNavigate();
  return (
    <>
      <Header />
      <div className="outer-container">
        <SideBar />
        <div className="inner-container">
          <Routes>
            <Route exact path="/" element={<Dashboard />} />
            <Route exact path="/dashboard" element={<Dashboard />} />
            <Route exact path="/people/add" element={<AddPeopleForm />} />
            <Route exact path="/logs/add" element={<AddLogsForm />} />
            <Route
              exact
              path="/grievance/select/:id"
              element={<SelectGrievance />}
            />
            <Route exact path="/logs/view/:id" element={<ViewLogs />} />
            <Route exact path="*" element={<Dashboard />} />
          </Routes>
        </div>
      </div>
      <Footer />
    </>
  );
};
export default Home;

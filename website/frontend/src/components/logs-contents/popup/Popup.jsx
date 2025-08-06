import React from "react";
import "./Popup.css"; // Optional: for styling

const Popup = ({ show, handleClose, children }) => {
  return (
    show && (
      <div className="popup-overlay">
        <div className="popup-content">
          <button className="close-button" onClick={handleClose}>
            &times;
          </button>
          {children}
        </div>
      </div>
    )
  );
};

export default Popup;

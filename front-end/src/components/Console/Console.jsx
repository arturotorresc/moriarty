import React from "react";
import "./style.css";

export function Console(props) {
  return (
    <div className="console-container">
      <textarea
        readOnly
        className="console-text"
        placeholder="no hay nada que ver..."
      ></textarea>
    </div>
  );
}

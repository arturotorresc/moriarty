import React from "react";
import "./styles.css";

export function Editor(props) {
  return (
    <div className="editor-container">
      <label className="editor-label" for="editor">
        Editor
      </label>
      <textarea id="editor" placeholder="Escribe el código aquí"></textarea>
      <button className="play-btn">PLAY</button>
    </div>
  );
}

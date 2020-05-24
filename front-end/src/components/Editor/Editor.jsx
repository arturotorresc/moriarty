import React from "react";
import { usePlayerId } from "../../hooks/usePlayerId";
import "./styles.css";

export function Editor(props) {
  const playerId = usePlayerId();
  console.log(playerId);
  return (
    <div className="editor-container">
      <label className="editor-label" htmlFor="editor">
        Editor
      </label>
      <textarea id="editor" placeholder="Escribe el código aquí"></textarea>
      <button className="play-btn">PLAY</button>
    </div>
  );
}

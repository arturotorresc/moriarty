import React, { useState } from "react";
import "./styles.css";
import { useFetch } from "../../hooks/useFetch";

export function Editor(props) {
  const [code, setCode] = useState("")
  const { post } = useFetch("/api/execute")
  const { get } = useFetch("/api/game-state")
  return (
    <div className="editor-container">
      <label className="editor-label" htmlFor="editor">
        Editor
      </label>
      <textarea id="editor" placeholder="Escribe el código aquí" onChange={ ev => {setCode(ev.target.value)} }></textarea>
      <button className="play-btn" 
        onClick = { ev => {
          post({ code }).then(() => {
            get().then(response => {
              props.updateGameState(response.data)
            }).catch(error => {
              console.log(error)
            })
          }).catch(error => {
            console.log(error)
          })
        }
       } > PLAY</button>
    </div>
  );
}

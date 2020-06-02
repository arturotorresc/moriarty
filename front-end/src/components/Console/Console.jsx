import React, { useState, useEffect } from "react";
import "./style.css";

export function Console(props) {
  const [logs, setLogs] = useState("")
  useEffect(() => {
    if (props.gameState && props.gameState.actions) {
      let actions = ""
      props.gameState.actions.forEach(element => {
        if (element[0] === "SPEAK") {
          actions += `${element[1]}: ${element[2]} \n`
        } else {
          actions += `${element[1]}: ${element[0]} ${element[2]} \n`
        }
      })
      console.log(actions, props.gameState)
      setLogs(actions)
    }
    console.log(props.gameState)
  }, [props.gameState])
  return (
    <div className="console-container">
      <textarea
        readOnly
        className="console-text"
        placeholder="no hay nada que ver..."
        defaultValue={logs}
      ></textarea>
    </div>
  );
}

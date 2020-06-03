import React from "react";
import "./style.css";
import { Button } from 'react-bootstrap';

export function Header(props) {
  return (
    <div className="header-container">
      <h1>Moriarty</h1>
      <div className="div-info"><Button className="floored" variant="outline-info" size="sm" onClick={() => {props.setShow(true)}}>Info</Button></div>
      <h3 className="floored">Por Jorge Arturo Torres y Ana Paola Treviño</h3>
    </div>
  );
}

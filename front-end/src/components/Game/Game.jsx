import React, { useEffect, useState } from "react";
import "./style.css";

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faUserNinja, faUserSecret, faUserTie, faUserAstronaut, faUserInjured,
          faGhost, faFlagCheckered, faFireAlt	} from '@fortawesome/free-solid-svg-icons'

const playerEmoji = [faUserNinja, faUserSecret, faUserTie, faUserAstronaut, faUserInjured]

export function Game(props) {
  let gameState = props.gameState;
  const [grid, setGrid] = useState([])
  useEffect(() => {
    if (gameState && gameState.map) {
      let array = new Array(gameState.map[0]).fill(0);
      let gridTemp = [];
      for(let i = 0; i < gameState.map[1]; i++) {
        gridTemp.push((<div className="row">{array.map((element, index) => {
          let content = "";
          if (index == gameState.goal[0] && i == gameState.goal[1]) {
            content = <FontAwesomeIcon icon={faFlagCheckered} />
          }
          gameState.players.forEach((element, player) => {
            if (index == element[1][0] && i == element[1][1]) {
              content = <FontAwesomeIcon icon={playerEmoji[player % 5]} />
            }
          });
          gameState.enemies.forEach(element => {
            if (index == element[0] && i == element[1]) {
              content = <FontAwesomeIcon icon={faGhost} />
            }
          });
          gameState.obstacles.forEach(element => {
            if (index == element[0] && i == element[1]) {
              content = <FontAwesomeIcon icon={faFireAlt} />
            }
          });
        return <div className="column">{content}</div>
        })}</div>));
      }
      setGrid(gridTemp);
    }
  }, [gameState])

  if (!gameState) {
    return null;
  }

  return <div className="game-container">
    {grid.map((row) => row)}
  </div>;
}

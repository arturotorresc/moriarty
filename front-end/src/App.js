import React, { useEffect, useState } from "react";
import { Header } from "./components/Header";
import { Editor } from "./components/Editor";
import { Console } from "./components/Console";
import { Game } from "./components/Game";
import { Instructions} from "./components/Modal";
import { useFetch } from "./hooks/useFetch";

import 'bootstrap/dist/css/bootstrap.css';
import "./App.css";

function App() {
  const { post } = useFetch("/api/new-game-state")
  const [gameState, setGameState] = useState({})
  const [show, setShow] = useState(true)

  useEffect(() => {
    post().then(response => {
      setGameState(response.data)
    }).catch(error => {
      console.log(error)
    })
  }, [])

  return (
    <div className="app-container">
      <header className="header">
        <Header setShow = { setShow } />
      </header>
      <section className="game">
        <Game gameState = { gameState } />
      </section>
      <main className="editor">
        <Editor updateGameState = { setGameState } />
      </main>
      <section className="console">
        <Console gameState = { gameState } />
      </section>
      <section className="instructions">
        <Instructions setShow = { setShow } show = { show } />
      </section>
    </div>
  );
}

export default App;

import React, { useEffect, useState } from "react";
import { Header } from "./components/Header";
import { Editor } from "./components/Editor";
import { Console } from "./components/Console";
import { Game } from "./components/Game";
import { useFetch } from "./hooks/useFetch";

import "./App.css";

function App() {
  const { post } = useFetch("/api/new-game-state")
  const [gameState, setGameState] = useState({})
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
        <Header />
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
    </div>
  );
}

export default App;

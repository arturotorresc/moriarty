import React from "react";
import { Header } from "./components/Header";
import { Editor } from "./components/Editor";
import { Console } from "./components/Console";
import { Game } from "./components/Game";
import "./App.css";

function App() {
  return (
    <div className="app-container">
      <header className="header">
        <Header />
      </header>
      <section className="game">
        <Game />
      </section>
      <main className="editor">
        <Editor />
      </main>
      <section className="console">
        <Console />
      </section>
    </div>
  );
}

export default App;

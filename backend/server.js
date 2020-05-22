const express = require("express");
const bodyParser = require("body-parser");
const morgan = require("morgan");
const shortid = require("shortid");
const fs = require("fs");
const process = require("process");
const { exec } = require("child_process");
const cors = require("cors");

const app = express();

app.use(morgan("dev"));
const jsonParser = bodyParser.json();
app.use(jsonParser);
app.use(cors());

// Sends an id for the user to send with their requests to
// identify their game files.
app.get("/api/user-id", (req, res) => {
  res.json({ id: shortid.generate() });
});

// Fetches the game state from the local files.
app.get("/api/game-state", (req, res) => {
  const { id } = req.body;
  fs.readFile(`./game_states/${id}_state.json`, "utf-8", (err, data) => {
    if (err) {
      console.log(err);
      return res.status(500).json({ error: err.message });
    }

    let jsonData = {};
    try {
      jsonData = JSON.parse(data);
    } catch (err) {
      console.log("Error while parsing JSON file", err);
      return res.status(500).json({ error: err.message });
    }
    return res.json({ ...jsonData });
  });
});

app.post("/api/execute", (req, res) => {
  const { code, id } = req.body;
  const fileName = `${id}_code.txt`;
  fs.writeFile(`./game_code/${fileName}`, code, { flag: "w" }, (err) => {
    if (err) {
      console.log(err);
      return res.status(500).json({ error: err.message });
    }
    console.log(`Moriarty code saved as: ${fileName} under game_code/`);
    process.chdir("../");
    console.log("Changed directory for Moriarty code execution");
    exec(
      `./moriarty.sh ./backend/game_code/${fileName}`,
      (err, stdout, stderr) => {
        if (err) {
          console.log("An error ocurred while executing code", err);
          return res.status(500).json({ error: err.message });
        }
        process.chdir("./backend");
        console.log("Code executed correctly");
        res.json({ stdout, stderr, message: "Code compiled and executed" });
      }
    );
  });
});

app.listen(4000, () => {
  console.log("Server successfully started at port 4000");
});

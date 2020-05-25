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

<<<<<<< Updated upstream
// Sends an id for the user to send with their requests to
// identify their game files.
app.get("/api/user-id", (req, res) => {
  res.json({ id: shortid.generate() });
=======
const GAME_STATE_FILE = "/game_states/game_state.json";

function getRandomInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min)) + min;
}

// Generates a game object and guarantees its not overwriting an already
// created object
function generateGameObjects(quantity, width, height, occupiedSpaces) {
  let gameObjects = [];
  const MAX_RETRIES = 15;
  let retries = 0;
  for (let i = 0; i < quantity; ++i) {
    if (retries == MAX_RETRIES) {
      break;
    }
    // We want to instantiate gameObjects starting from the second row and not be
    // in the last row, as players go in the first row and the target is in the
    // last goal
    const x = getRandomInt(0, width - 1);
    const y = getRandomInt(1, height - 1);
    let alreadyThere = gameObjects.find((pos) => pos[0] == x && pos[1] == y);
    alreadyThere = occupiedSpaces.find((pos) => pos[0] == x && pos[1] == y);
    if (alreadyThere) {
      // Retry attempt
      i -= 1;
      retries += 1;
      continue;
    }
    gameObjects.push([x, y]);
  }
  return gameObjects;
}

// Generates a new game.
app.post("/api/new-game-state", (req, res) => {
  let width = getRandomInt(4, 14);
  let height = getRandomInt(4, 14);
  let enemies = generateGameObjects(getRandomInt(1, 3), width, height, []);
  let obstacles = generateGameObjects(
    getRandomInt(1, width - 2),
    width,
    height,
    enemies
  );
  let gameState = {
    map: [width, height],
    // Empty players because we don't know how many players there'll be
    players: [],
    // Array of remaining ammo for each player
    ammo: [],
    // Direction to which each player is looking
    players_direction: [],
    // Enemies locations (varies between 1 and 3 enemies).
    enemies,
    obstacles,
    actions: [],
    // Generates the goal in the last row
    goal: [getRandomInt(0, width), getRandomInt(height - 2, height - 1)],
  };
  fs.writeFile(
    __dirname + GAME_STATE_FILE,
    JSON.stringify(gameState),
    { code: "w " },
    (err) => {
      if (err) {
        return res.status(500).json({ error: err.message });
      }
      res.json(gameState);
    }
  );
>>>>>>> Stashed changes
});

// Fetches the game state from the local files.
app.get("/api/game-state", (req, res) => {
<<<<<<< Updated upstream
  const { id } = req.body;
  fs.readFile(`./game_states/${id}_state.json`, "utf-8", (err, data) => {
=======
  fs.readFile(__dirname + GAME_STATE_FILE, "utf-8", (err, data) => {
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
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
=======
  const { code } = req.body;
  const fileName = "code.txt";
  fs.writeFile(
    __dirname + `/game_code/${fileName}`,
    code,
    { flag: "w" },
    (err) => {
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
            process.chdir("./backend");
            return res.status(500).json({ error: err.message });
          }
          process.chdir("./backend");
          console.log("Code executed correctly");
          res.json({ stdout, stderr, message: "Code compiled and executed" });
        }
      );
    }
  );
>>>>>>> Stashed changes
});

app.listen(4000, () => {
  console.log("Server successfully started at port 3000");
});

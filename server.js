const dns = require('dns').promises;
const os = require('os');
const express = require("express");
const sqlite3 = require('sqlite3').verbose();
const osName = os.hostname(); // Get the hostname of the current machine
const {createServer} = require('http');
const {Server} = require('socket.io');


async function getIPAddress() {
  try {
    const { address } = await dns.lookup(osName, { family: 4 });
    return address;
  } catch (err) {
    console.error(`Error resolving hostname: ${err}`);
    return null;
  }
}

async function startServer() {
  const ipAddress = await getIPAddress();
  if (!ipAddress) {
    console.error('Could not determine IP address. Server not started.');
    return;
  }

  // Connect to DB
  let db = new sqlite3.Database('./db/NODEMCU.db', sqlite3.OPEN_READWRITE, err => {
    if (err) return console.error(err.message)
  })

  db.serialize(()=> {
    // Create table with a date column
    db.run("CREATE TABLE IF NOT EXISTS templogs (id INTEGER PRIMARY KEY AUTOINCREMENT, name, temperature REAL, created_at TEXT)");
  })

  // Server initialization
  const port = 3000;
  const app = express();
  app.use(express.json());

  const httpServer = createServer(app)
  const io = new Server(httpServer, {
    cors: {
      origin: "*"
    },
  })

  // Handle socket connection
  io.on('connection', (socket) => {
    console.log('New client connected');
    socket.on('disconnect', () => {
      console.log('Client disconnected');
    });
  });

  // Server endpoints
  app.get("/", (req, res) => {
    res.send(`Server running at http://${ipAddress}:${port}/`)
  })

  app.get("/templogs", (req, res) => {
    db.all("SELECT * FROM templogs ORDER BY created_at DESC LIMIT ?", [15], (err, rows) => {
      if (err) {
        console.error(err.message);
        res.status(500).json({ message: "Error retrieving data from the database" });
        return;
      }
      res.status(200).json(rows);
    });
  });

  app.get("/templogs/week", (req, res) => {
    db.all(
      "SELECT * FROM templogs WHERE created_at >= DATETIME('now', '-7 days') ORDER BY created_at DESC",
      [],
      (err, rows) => {
        if(err) {
          console.error(err.message);
          res.status(500).json({ message: "Error retrieving data from the database" });
          return;
        }
        res.status(200).json(rows);
      }
    );
  });

  app.get("/templogs/day", (req, res) => {
    db.all(
      "SELECT * FROM templogs WHERE created_at >= DATETIME('now', '-1 day') ORDER BY created_at DESC",
      [],
      (err, rows) => {
        if(err) {
          console.error(err.message);
          res.status(500).json({ message: "Error retrieving data from the database" });
          return;
        }
        res.status(200).json(rows);
      }
    )
  })

  app.get("/templogs/hour", (req, res) => {
    db.all(
      "SELECT * FROM templogs WHERE created_at >= DATETIME('now', '-1 hour') ORDER BY created_at DESC",
      [],
      (err, rows) => {
        if(err) {
          console.error(err.message);
          res.status(500).json({ message: "Error retrieving data from the database" });
          return;
        }
        res.status(200).json(rows);
      }
    )
  })
  

  app.post("/", (req, res) => {
    const data = req.body;

    console.log("Data received: ", data);

    if (!data || !data.name || !data.temperature) {
      res.status(400).json({ message: "Invalid data, missing a field" });
      return;
    }

    const name = data.name;
    const value = data.temperature;
    const createdAt = new Date().toISOString(); // Current date in ISO format (YYYY-MM-DDTHH:MM:SS.sssZ)

    // Insert data into the templogs table
    db.run(
      "INSERT INTO templogs (name, temperature, created_at) VALUES (?, ?, ?)",
      [name, value, createdAt],
      function (err) {
        if (err) {
          console.error(err.message);
          res.status(500).json({ message: "Error inserting data into the database" });
        } else {
          console.log(`A row has been inserted with rowid ${this.lastID}`);
          res.status(200).json({
            message: "Data inserted successfully",
            rowId: this.lastID,
          });

          // Socket boardcast of data to all connected users
          io.emit("logsupdate", {
            id: this.lastID,
            name: name,
            temperature: value,
            created_at: createdAt,
          })
        }
      }
    );
  });

  httpServer.listen(port, '0.0.0.0', () => {
    console.log(`Server initialized`);
    console.log(`Server running at http://${ipAddress}:${port}/`)
  });
}

startServer();

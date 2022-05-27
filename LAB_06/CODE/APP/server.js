const express = require("express");
const cors = require("cors");
const { spawn } = require("child_process");

const data = require("./data.json");

const findBestDocuments = async (req, res) => {
  try {
    const { query, k } = req.body;
    console.log(query);
    console.log(k);
    // const childPython = spawn("python", ["zad7.py", query, k]);
    const childPython = spawn("python", ["zad8.py", query, k]);
    childPython.stdout.on("data", (data) => {
      // data = data.toString();
      // data = data.split("");
      // data[1] = '"';
      // for (let i = 2; i < data.length - 1; i++) {
      //   if (data[i] == "'" && data[i + 1] == ",") data[i] = '"';
      //   else if (data[i] == "'" && data[i - 1] == " " && data[i - 2] == ",")
      //     data[i] = '"';
      //   else if (data[i] == "'" && data[i + 1] == "]") data[i] = '"';
      // }
      // data = data.join("");
      console.log(`stdout: ${data}`);
      res.status(200).json({ action: "Success", documents: `${data}` });
    });

    childPython.stderr.on("data", (data) => {
      console.error(`stderr: ${data}`);
      res.status(500).json({ action: "Something wrong" });
    });

    // childPython.on("close", (code) => {
    //   console.log(`child process exited with code ${code}`);
    // });
  } catch (err) {
    res.status(500).json({ action: "Something wrong" });
  }
};

const getDocumentsTitles = async (req, res) => {
  try {
    const { indexes } = req.body;
    console.log(indexes);
    let a = JSON.parse(indexes);
    let titles = [];
    for (let index of a) titles.push(data[index].title);
    res.status(200).json({ action: "Success", titles: JSON.stringify(titles) });
  } catch (err) {
    res.status(500).json({ action: "Something wrong" });
  }
};

const getDocument = async (req, res) => {
  try {
    const { title } = req.body;
    console.log(title);
    let obj = data.find((x) => x.title == title);
    res
      .status(200)
      .json({ action: "Success", content: JSON.stringify(obj.content) });
  } catch (err) {
    res.status(500).json({ action: "Something wrong" });
  }
};

const app = express();
app.use(
  cors({
    credentials: true,
    origin: "http://localhost:3000",
  })
);
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.post("/search", findBestDocuments);
app.post("/getDocumentsTitles", getDocumentsTitles);
app.post("/getDocument", getDocument);

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
  console.log(`SERVER RUNNING ON PORT ${PORT}`);
});

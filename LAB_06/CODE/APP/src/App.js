import React, { Component } from "react";
import Navbar from "./components/Navbar";
import Document from "./components/Document";

import "./App.css";

export default class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      documents: [],
      content: "",
      title: "",
    };
  }

  setDocuments = (documents) => {
    this.setState({
      documents: documents,
      content: "",
      title: "",
    });
  };

  setContent = (title, content) => {
    this.setState({
      content: content,
      title: title,
    });
  };

  showDocument = (title) => {
    console.log(title);
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: title }),
    };
    fetch("http://localhost:5000/getDocument", requestOptions)
      .then((response) => response.json())
      .then((data) => {
        if (data.action === "Success") {
          this.setContent(title, data.content);
        }
      });
  };

  render() {
    let documents = this.state.documents;
    let docs = [];
    for (let i = 0; i < documents.length; i++) {
      let text = `DOC${i}`;
      docs.push(
        <Document
          key={text}
          text={documents[i]}
          showDocument={this.showDocument}
        />
      );
    }

    return (
      <div>
        <Navbar setDocuments={this.setDocuments} />
        <div id="results">
          <div className="searchedDocuments">{docs}</div>
          <div className="documentContent">
            <div id="title">{this.state.title}</div>
            <div id="content">{this.state.content}</div>
          </div>
        </div>
      </div>
    );
  }
}

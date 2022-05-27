import React, { Component } from "react";

import "./SearchPanel.css";

class SearchInput extends Component {
  constructor(props) {
    super(props);
    this.state = {
      query: "",
      k: 10,
    };

    this.handleInput = this.handleInput.bind(this);

    this.handleSelect = this.handleSelect.bind(this);
  }

  handleInput = (e) => {
    this.setState({ query: e.target.value });
  };

  handleSelect = (e) => {
    this.setState({ k: e.target.value });
  };

  handleClick = (e) => {
    if (e.keyCode === 13) this.handleSearch();
  };

  getDocumentsAtIndexes = (indexes) => {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ indexes: JSON.stringify(indexes) }),
    };
    fetch("http://localhost:5000/getDocumentsTitles", requestOptions)
      .then((response) => response.json())
      .then((data) => {
        if (data.action === "Success") {
          console.log(data.titles);
          const titles = JSON.parse(data.titles);
          this.props.setDocuments(titles);
        }
      });
  };

  handleSearch = () => {
    console.log(this.state.query, this.state.k);
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: this.state.query, k: this.state.k }),
    };
    fetch("http://localhost:5000/search", requestOptions)
      .then((response) => response.json())
      .then((data) => {
        if (data.action === "Success") {
          console.log(data.documents);
          const indexes = JSON.parse(data.documents);
          this.getDocumentsAtIndexes(indexes);
        }
      });
  };

  render() {
    const start = 10;
    const end = 400;
    let options = [];
    for (let i = start; i <= end; i++) {
      let key = `opt${i}`;
      options.push(
        <option key={key} value={i}>
          {i}
        </option>
      );
    }

    return (
      <div id="searchPanel">
        <select id="searchSelect" onChange={this.handleSelect}>
          {options}
        </select>
        <input
          id="searchInput"
          type="text"
          placeholder="Search"
          spellCheck={false}
          value={this.state.value}
          onChange={this.handleInput}
          onKeyDown={this.handleClick}
        />
        <button id="searchButton" onClick={this.handleSearch}>
          Search
        </button>
      </div>
    );
  }
}

export default SearchInput;

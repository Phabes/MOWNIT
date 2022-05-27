import React, { Component } from "react";

import "./Navbar.css";
import SearchPanel from "./SearchPanel";

class Navbar extends Component {
  render() {
    return (
      <nav>
        <SearchPanel setDocuments={this.props.setDocuments} />
      </nav>
    );
  }
}

export default Navbar;

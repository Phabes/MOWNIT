import React, { Component } from "react";
import PropTypes from "prop-types";

import "./Document.css";

class Document extends Component {
  render() {
    return (
      <div
        className="singleDocument"
        onClick={() => this.props.showDocument(this.props.text)}
      >
        {this.props.text}
      </div>
    );
  }
}

Document.propTypes = {
  text: PropTypes.string,
};

export default Document;

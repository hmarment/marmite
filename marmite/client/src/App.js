import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

import axios from 'axios';

class App extends Component {

  constructor() {
    super();
  };

  componentDidMount() {
    this.getRecipes();
  };

  getRecipes() {
    axios.get(`${process.env.REACT_APP_BACKEND_URL}/api/ext/guardian/list`)
    .then((res) => { console.log(res.data.data); })  // new
    .catch((err) => { console.log(err); })
  };

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <p>
            Edit <code>src/App.js</code> and save to reload.
          </p>
          <a
            className="App-link"
            href="https://reactjs.org"
            target="_blank"
            rel="noopener noreferrer"
          >
            Learn React
          </a>
        </header>
      </div>
    );
  }
}

export default App;

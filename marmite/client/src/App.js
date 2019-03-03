import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import Feed from './components/Feed';

import axios from 'axios';

class App extends Component {

  constructor() {
    super();
    this.state = {
      recipes: []
    };
  };

  componentDidMount() {
    this.getRecipes();
  };

  getRecipes() {
    axios.get(`${process.env.REACT_APP_BACKEND_URL}/api/ext/guardian/list`)
    .then((res) => { this.setState({ recipes: res.data }); })  // new
    .catch((err) => { console.log(err); })
  };

  render() {
    return (
      <div className="App">
        <header>
          <h1> Marmite </h1>
          <h3> You Either Love It or Hate It. </h3>
        </header>
        <Feed recipes={this.state.recipes}/>
      </div>
    );
  }
}

export default App;

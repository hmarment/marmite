import React, { Component } from 'react';
// import logo from './logo.svg';
import 'bootstrap/dist/css/bootstrap.css';
import './App.css';
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import Feed from './components/Feed';

import axios from 'axios';

class App extends React.Component {

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
    axios.get(`${process.env.REACT_APP_BACKEND_URL}/api/recipes/`)
    .then((res) => { this.setState({ recipes: res.data }); })  // new
    .catch((err) => { console.log(err); })
  };

  render() {
    return (
      <div className="App">
      <Container>
        <Navbar bg="dark" variant="dark">
          <Navbar.Brand href="#home">Marmite</Navbar.Brand>
          <Navbar.Toggle />
          <Navbar.Collapse className="justify-content-end">
            <Navbar.Text>
              <i>You Either Love It Or Hate It.</i>
            </Navbar.Text>
          </Navbar.Collapse>
          </Navbar>
          <div>
            <Feed recipes={this.state.recipes}/>
          </div>
        </Container>
      </div>
    );
  }
}

export default App;

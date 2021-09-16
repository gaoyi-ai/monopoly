// import logo from './logo.svg';
import React, { Component } from 'react'
import './App.css';
import { Route, Switch } from 'react-router-dom';
import Login from './components/Login/Login.js';
import Register from './components/Register/Register.js';
import Join from './components/Join/Join.js';
import Gameboard from './components/Gameboard/Gameboard';

class App extends Component {
  render() {
    return (
      <div >
        <Switch>
          <Route path='/register' component={Register}></Route>
          <Route path="/join" component={Join}></Route>
          <Route path="/gameboard" component={Gameboard}></Route>
          <Route component={Login}></Route>
        </Switch>
      </div>
    );
  }
}

export default App;

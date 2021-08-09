import './App.css';
import React from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import CreateExercisePage from './pages/CreateExercisePage';
import EditExercisePage from './pages/EditExercisePage';

function App() {
  return (
    <div className="App">
      <Router>
        <header className="App-header">
          <Route path='/' exact>
            <HomePage />
          </Route>
          <Route path='/create-exercise'>
            <CreateExercisePage />
          </Route>
          <Route path='/edit-exercise'>
            <EditExercisePage />
          </Route>
        </header>
      </Router>
    </div>
  );
}

export default App;

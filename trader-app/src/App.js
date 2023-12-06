import './App.css';
import React from 'react';
import { BrowserRouter as Router, Route, Switch, Routes } from 'react-router-dom';
import Trade from './pages/trade';
import Train from './pages/train';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Trade/>} />
        <Route path="/train" element={<Train/>} />
      </Routes>
    </Router>
  );
}

export default App;

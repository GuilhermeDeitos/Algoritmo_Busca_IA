import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import React from 'react';

import MyGridAuto from './components/gridauto.js'
import MyGridManual from './components/gridmanual.js'

import './app.css'

export default function App() {
  return (
    <Router>
      <div className="App">
        <nav>
            <ul>
              <li>
                <Link to="/">Grid automatica</Link>
              </li>
              <li>
                <Link to="/manual">grid manual</Link>
              </li>
            </ul>
        </nav>
        <Routes>
          <Route path="/" element={<MyGridAuto/>} />
          <Route path="/manual" element={<MyGridManual/>} />
        </Routes>
      </div>
      </Router>
  );
}

import './App.css';
import CreateEventPage from './components/CreateEventPage';
import DashboardPage from './components/DashboardPage';
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';


function App() {
  return (
    <Router>
      <Routes>
        {/* Main Organization Dashboard Page after login */}
        <Route path="/dashboard" element={<DashboardPage />} />
        {/* Create Event Page */}
        <Route path="/create-event" element={<CreateEventPage />} />
      </Routes>
    </Router>
  );
}

export default App;

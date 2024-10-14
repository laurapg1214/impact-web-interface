import './App.css';
import EventCreatePage from './components/EventCreatePage';
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
        <Route path="/event-create" element={<EventCreatePage />} />
      </Routes>
    </Router>
  );
}

export default App;

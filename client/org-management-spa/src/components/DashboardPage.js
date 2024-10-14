import React from 'react';
import { Link } from 'react-router-dom';

const DashboardPage = () => {
    return (
        <div>  
            {/* ***TODO***: dynamically insert Org name before 'Dashboard' */}
            <h1>Dashboard</h1>
            <p>Welcome to the [ORGANIZATION NAME] Dashboard</p>
            {/* Link to Create Event page */}
            <Link to="/event-create">Create a New Event</Link>
        </div>
    );
};

export default DashboardPage;
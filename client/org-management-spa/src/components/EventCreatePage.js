import React, { useState } from 'react';

const EventCreatePage = () => {
    const [eventName, setEventName] = useState('');
    const [eventDescription, setEventDescription] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        const eventData = { 
            name: eventName,
            description: eventDescription
        };

        try {
            const response = await fetch(
                'http://localhost:8000/api/events/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(eventData),
                }
            );

            if (response.ok) {
                alert('Event created successfully!');
            } else {
                alert('Failed to create event');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <div>
            <h2>Create a New Event</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Event Name:</label>
                    <input
                        type="text"
                        value={eventName}
                        onChange={(e) => setEventName(e.target.value)}
                    />
                </div>
                <div>
                    <label>Event Description:</label>
                    <textarea
                        value={eventDescription}
                        onChange={(e) => setEventDescription(e.target.value)}
                    ></textarea>
                </div>
                <button type="submit">Create Event</button>
            </form>
        </div>
    );
};

export default EventCreatePage;
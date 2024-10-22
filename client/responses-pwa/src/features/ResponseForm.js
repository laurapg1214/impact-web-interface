import { useState } from 'react';

function ResponseForm({ eventId, questionId }) {
    const [response, setResponse] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();

        fetch(`/api/events/${eventId}/questions/${questionId}/response`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ response }),
        })
            .then((res) => res.json())
            .then((data) => {
                alert('Thank you for submitting your response!');
                setResponse('');
            });
    };

    return (
        <form onSubmit={handleSubmit}>
            <textarea
                value={response}
                onChange={(e) => setResponse(e.target.value)}
                placeholder="Please enter your response here"
            />
            <button type="submit">Submit</button>
        </form>
    );
}

export default ResponseForm;
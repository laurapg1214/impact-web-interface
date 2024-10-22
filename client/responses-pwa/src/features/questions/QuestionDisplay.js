// fetches current question from backend api & displays it //

import { useEffect, useState } from 'react';

function QuestionPrompt({ eventId }) {
    const [question, setQuestion] = useState(null);

    useEffect(() => {
        // fetch the question from backend api using the event ID
        fetch(`/api/events/${eventId}/current-question`)
            .then((response) => response.json())
            .then((data) => setQuestion(data.question));
    } [eventId]);

    return (
        <div>
            {question ? <p>{question}</p> : <p>Loading question...</p>}
        </div>
    );
}

export default QuestionPrompt;
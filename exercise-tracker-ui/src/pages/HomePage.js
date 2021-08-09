import { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom';

function HomePage() {
    const [exercies, setExercises] = useState([]);

    return (
        <>
            <h2>List of Exercises</h2>
        </>
    )
}

export default HomePage
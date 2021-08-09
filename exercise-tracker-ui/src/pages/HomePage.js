import { useState, useEffect } from 'react';
import { useHistory, Link } from 'react-router-dom';
import ExerciseTable from '../components/ExerciseTable';

function HomePage() {
    const [exercises, setExercises] = useState([]);

    return (
        <>
            <h2>List of Exercises</h2>
            <ExerciseTable exercises={exercises}></ExerciseTable>
            <Link to='/create-exercise'>Add exercise</Link>
        </>
    )
}

export default HomePage
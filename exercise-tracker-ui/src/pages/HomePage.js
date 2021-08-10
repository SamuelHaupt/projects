import React, { useState, useEffect } from 'react';
import { useHistory, Link } from 'react-router-dom';
import ExerciseTable from '../components/ExerciseTable';

function HomePage({ setExerciseToEdit }) {
    const [exercises, setExercises] = useState([]);
    const history = useHistory();

    const onDelete = async id => {
        const response = await fetch(`/exercises/${id}`, { method: 'DELETE' });
        if (response.status === 204) {
            const getResponse = await fetch('/exercises');
            const exercises = await getResponse.json();
            setExercises(exercises);
        } else {
        console.error(`Failed to delete the exercise with id = ${id}, status code = ${response.status}`)
        }
    }	

    const onEdit = exercise => {
        setExerciseToEdit(exercise);
        history.push('/edit-exercise');
    }

    const loadExercises = async () => {
        const response = await fetch('/exercises');
        const data = await response.json();
        setExercises(data);
    }

    useEffect(() => {
        loadExercises();
    }, []);

    return (
        <>
            <h2>List of Exercises</h2>
            <ExerciseTable exercises={exercises} onDelete={onDelete} onEdit={onEdit}></ExerciseTable>
            <Link to='/create-exercise'>Add exercise</Link>
        </>
    )
}

export default HomePage
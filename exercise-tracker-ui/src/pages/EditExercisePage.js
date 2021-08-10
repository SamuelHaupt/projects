import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
import UnitDefaultSelectForm from '../components/UnitDefaultSelectForm';


function EditExercisePage ({ exerciseToEdit }) {
    const [name, setName] = useState(exerciseToEdit.name);
    const [reps, setReps] = useState(exerciseToEdit.reps);
    const [weight, setWeight] = useState(exerciseToEdit.weight);
    const [unit, setUnit] = useState(exerciseToEdit.unit);
    const [date, setDate] = useState(exerciseToEdit.date);

    const history = useHistory();

    const editExercise = async () => {
        const editedExercise = { name, reps, weight, unit, date };
        const response = await fetch(`exercises/${exerciseToEdit._id}`, {
            method: 'PUT',
            body: JSON.stringify(editedExercise),
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.status === 200) {
            alert('Successfully edited the exercise.');
            history.push('/');
        } else {
            alert(`Failed to edit exercise. Status code ${response.status}`);
        }
    };

    return (
        <div>
            <h1>Edit Exercise</h1>
            <table id='exercises'>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Reps</th>
                        <th>Weight</th>
                        <th>Unit</th>
                        <th>Date</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <th><input
                            type='text'
                            value={name}
                            onChange={input => setName(input.target.value)} />
                        </th>
                        <th><input
                            type='number'
                            value={reps}
                            onChange={input => setReps(input.target.value)} />
                        </th>
                        <th><input
                            type='Number'
                            value={weight}
                            onChange={input => setWeight(input.target.value)} />
                        </th>
                        <th>
                            <UnitDefaultSelectForm unit={unit} setUnit={setUnit} />
                        </th>
                        <th><input
                            type='text'
                            value={date}
                            onChange={input => setDate(input.target.value)} />
                        </th>
                    </tr>
                </tbody>
            
            </table>
            <br />
            <button
                onClick={editExercise}
            >Save</button>
        </div>
    )
}




export default EditExercisePage;
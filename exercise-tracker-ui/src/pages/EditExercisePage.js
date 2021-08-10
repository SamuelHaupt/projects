import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
import EditSelectUnit from '../components/EditSelectUnit';


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
                    <tr class='ModifyRow'>
                        <td><input
                            type='text'
                            value={name}
                            onChange={input => setName(input.target.value)} />
                        </td>
                        <td><input
                            type='number'
                            value={reps}
                            onChange={input => setReps(input.target.value)} />
                        </td>
                        <td><input
                            type='Number'
                            value={weight}
                            onChange={input => setWeight(input.target.value)} />
                        </td>
                        <td>
                            <EditSelectUnit unit={unit} setUnit={setUnit} />
                        </td>
                        <td><input
                            type='text'
                            value={date}
                            onChange={input => setDate(input.target.value)} />
                        </td>
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
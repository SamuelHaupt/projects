import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';

function CreateExercisePage () {
    const [name, setName] = useState('');
    const [reps, setReps] = useState('');
    const [weight, setWeight] = useState('');
    const [unit, setUnit] = useState('');
    const [date, setDate] = useState('');

    const history = useHistory();

    const createExercise = async () => {
        const newExercise = {name, reps, weight, unit, date};
        const response = await fetch('/exercises', {
            method: 'POST',
            body: JSON.stringify(newExercise),
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.status === 201) {
            alert('Successfully added the exercise.');
            history.push('/');
        } else {
            if (Object.values(response.body).length < 5) {
                alert('Field inputs are incorrect. Supply correct inputs to all fields.');
            } else {
                alert(`Failed to add exercise. Status code ${response.status}`);
            }
        }
        
    };

    return (
        <div>
            <h1>Add Exercise</h1>
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
                    <tr className='ModifyRow'>
                        <td>
                            <input
                            type='text'
                            value={name}
                            onChange={input => setName(input.target.value)} />
                        </td>
                        <td>
                            <input
                            type='number'
                            value={reps}
                            onChange={input => setReps(input.target.value)} />
                        </td>
                        <td>
                            <input
                            type='Number'
                            value={weight}
                            onChange={input => setWeight(input.target.value)} />
                        </td>
                        <td>
                            <select name='createUnit' onChange={input => setUnit(input.target.value)}>
                                <option value='' selected disabled hidden>Select</option>
                                <option value='lbs' >lbs</option>
                                <option value='kgs'>kgs</option>
                            </select>
                        </td>
                        <td>
                            <input
                            type='text'
                            value={date}
                            onChange={input => setDate(input.target.value)} />
                        </td>
                    </tr>
                </tbody>
            
            </table>
            <br />
            <button
                onClick={createExercise}
            >Save</button>
        </div>
    )
}

export default CreateExercisePage;
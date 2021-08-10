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
        console.log(response.body)
        if (response.status === 201) {
            alert('Successfully added the exercise.');
            history.push('/');
        } else {
            if (Object.values(response.body).length < 5) {
                alert('Fields are missing. Supply inputs to all fields.');
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
                            <select name='createUnit' onChange={input => setUnit(input.target.value)}>
                                <option value='' selected disabled hidden>Select</option>
                                <option value='lbs' >lbs</option>
                                <option value='kgs'>kgs</option>
                            </select>
                        </th>
                        <th>
                            <input
                            type='text'
                            value={date}
                            onChange={input => setDate(input.target.value)} />
                        </th>
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
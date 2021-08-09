import React from 'react';
import ExerciseTableItem from './ExerciseTableItem';

function ExerciseTable({exercises}) {
    return (
        <table id='exercises'>
            <thead>
                <tr>
                    <th>Exercise Name</th>
                    <th>Repetitions</th>
                    <th>Weight</th>
                    <th>Unit of Measurement</th>
                    <th>Date</th>
                    <th>Edit</th>
                    <th>Delete</th>
                </tr>
            </thead>
            <tbody>
                {exercises.map((exercise, index) =>
                    <ExerciseTableItem exercise={exercise}
                        key={index} />)}
            </tbody>
        </table>
    );
}

export default ExerciseTable
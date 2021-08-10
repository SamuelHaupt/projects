import React from 'react';
import ExerciseTableItem from './ExerciseTableItem';

function ExerciseTable({exercises, onDelete, onEdit}) {
    return (
        <table>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Reps</th>
                    <th>Weight</th>
                    <th>Unit</th>
                    <th>Date</th>
                    <th class='BlankColumn'></th>
                    <th class='BlankColumn'></th>
                </tr>
            </thead>
            <tbody>
                {exercises.map((exercise, index) =>
                    <ExerciseTableItem
                        exercise={exercise}
                        onDelete={onDelete}
                        onEdit={onEdit}
                        key={index} />)}
            </tbody>
        </table>
    );
}

export default ExerciseTable
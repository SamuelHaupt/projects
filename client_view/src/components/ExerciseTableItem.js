import React from 'react';
import { MdDeleteForever, MdEdit } from 'react-icons/md';

function ExerciseTableItem({exercise, onDelete, onEdit}) {
    return (
        <tr>
            <td>{exercise.name}</td>
            <td>{exercise.reps}</td>
            <td>{exercise.weight}</td>
            <td>{exercise.unit}</td>
            <td>{exercise.date}</td>
            <td><MdEdit className='EditIcon' onClick={ () => onEdit(exercise)}/></td>
            <td><MdDeleteForever className='DeleteIcon' onClick={ () => onDelete(exercise._id)} /></td>
        </tr>
    )
}

export default ExerciseTableItem
import React from 'react';

function EditSelectUnit ({ unit, setUnit }) {
    
        return (
            <>
                <select defaultValue={unit} onChange={input => setUnit(input.target.value)}>
                    <option value='lbs'>lbs</option>
                    <option value='kgs'>kgs</option>
                </select>
            </>
        );
    
}






export default EditSelectUnit








// <label for='selectUnit'>Unit of Measurement</label>
//             <select name='unit' id='selectUnit'>
                
//                 <option value='Lbs'>Lbs</option>
//                 <option value='Kgs'>Kgs</option>
//             </select>
//                 type='text'
//                 value={unit}
//                 onChange={input => setUnit(input.target.value)} />

//                 const defaultUnit = () => {
//                     if (unit === 'Lbs') {
//                         return {
//                             `<option value='Lbs' selected>Lbs</option>`
//                             `<option value='Kgs'>Kgs</option>`
//                         };
//                     } else {
//                         return {
//                             `<option value='Lbs'>Lbs</option>
//                             <option value='Kgs' selected>Kgs</option>`
//                         };
//                     }
//                 }
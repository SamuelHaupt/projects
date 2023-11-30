import React, { useEffect, useState } from 'react';
import axios from 'axios';


function TrainSide() {
    const [start, setStart] = useState('2021-01-01')
    const [end, setEnd] = useState('2021-01-01')

    const handleStartChange = (event) => {
        setStart(event.target.value);
    };

    const handleEndChange = (event) => {
        setEnd(event.target.value);
    };

    const handleTrainClick = () => {
        const startDate = new Date(start);
        const endDate = new Date(end);
        const yesterday = new Date();
        yesterday.setDate(yesterday.getDate() - 1);
        if (startDate > endDate) {
            alert('Start date cannot be later than the end date.');
            return;
        }
        if (endDate > yesterday) {
            alert('End date cannot be later than yesterday.');
            return;
        }
        if (startDate === endDate) {
            alert('Start date cannot be the same as the end date.');
            return;
        }
        axios.post('http://localhost:5000/run_trainer', { start: start, end: end })
            .then(response => {
                if (response.data.status === 'Success') {
                    console.log('Trade started successfully');
                    alert('Trade started successfully');
                }
            })
            .catch(error => console.error('Error starting trade:', error));
    };

    return (
        <section id="trainside-sec">
            <div className="start-input-container">
                <p>Start</p>
                <input type="date" id="start-input" value={start} onChange={handleStartChange}></input>
            </div>
            <div className="end-input-container">
                <p>End</p>
                <input type="date" id="end-input" value={end} onChange={handleEndChange}></input>
            </div>
            <div className="train-button-container">
                <button id="train" onClick={handleTrainClick}>Train</button>
            </div>
        </section>
    )
}

export default TrainSide;
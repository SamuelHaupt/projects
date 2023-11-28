import React, { useState, useEffect } from 'react';
import axios from 'axios';

function TrainOutput() {
    const [output, setOutput] = useState('');

    useEffect(() => {
        const interval = setInterval(() => {
            axios.get('http://localhost:5000/get_console_output')
                 .then(response => {
                     setOutput(response.data.output);
                 })
                 .catch(error => {
                     console.error('Error fetching data: ', error);
                 });
        }, 3000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div id="train-output-container">
            <h1>Training and Decision Output</h1>
            <div id="train-output">
                <pre>{output}</pre>
            </div>
        </div>
    );
}

export default TrainOutput;
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Header from '../components/HeaderS';
import TrainSide from '../components/TrainSide';
import Footer from '../components/Footer';
import TrainOutput from '../components/TrainOutput';

function ConsoleOutput() {
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
        }, 2000);

        return () => clearInterval(interval);
    }, []);

    return (
        <div className='container'>
            <header className="header">
                <Header/>
            </header>
            <section className='content'>
                <TrainOutput/>
            </section>
            <aside className='sidebar'>
                <TrainSide/>
            </aside>
            <Footer/>
        </div>
    );
}

export default ConsoleOutput;

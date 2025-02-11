import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Header from '../components/HeaderS';
import TrainSide from '../components/TrainSide';
import Footer from '../components/Footer';
import TrainOutput from '../components/TrainOutput';

const Train = () => {
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

export default Train;

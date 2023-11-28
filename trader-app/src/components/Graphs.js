import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS } from 'chart.js/auto';

function Graphs() {
    const [monthlyHistory, setMonthlyHistory] = useState({ labels: [], data: [] });
    const [quarterlyHistory, setQuarterlyHistory] = useState({ labels: [], data: [] });

    useEffect(() => {
        axios.get('http://localhost:5000/get_monthly_history')
            .then(response => {
                if (response.data && response.data.monthly_history) {
                    const history = response.data.monthly_history;
                    const labels = Object.keys(history).map(key => key.split('-')[2]);
                    const data = Object.values(history); 
                    setMonthlyHistory({ labels, data });
                }
            })
            .catch(error => console.error('Error fetching monthly history:', error));
    }, []);
    
    useEffect(() => {
        axios.get('http://localhost:5000/get_quarterly_history')
            .then(response => {
                if (response.data && response.data.quarter_history) {
                    const history = response.data.quarter_history;
                    const labels = Object.keys(history).map(key => key.split('-')[1]);
                    const data = Object.values(history); 
                    setQuarterlyHistory({ labels, data });
                }
            })
            .catch(error => console.error('Error fetching quarterly history:', error));
    }
    , []);

    const data = {
        labels: monthlyHistory.labels,
        datasets: [
            {
                label: 'Monthly Asset Prices',
                data: monthlyHistory.data,
                fill: false,
                backgroundColor: 'rgb(75, 192, 192)',
                borderColor: 'rgba(75, 192, 192, 0.2)',
            },
        ],
    };

    const data2 = {
        labels: quarterlyHistory.labels,
        datasets: [
            {
                label: 'Quarterly Asset Prices',
                data: quarterlyHistory.data,
                fill: false,
                backgroundColor: 'rgb(75, 192, 192)',
                borderColor: 'rgba(75, 192, 192, 0.2)',
            },
        ],
    };

    const options = {
        maintainAspectRatio: false,
    };

    return (
        <section className="graph-section">
            <figure className="graphs" id="graph1">
                <Line data={data} options={options} />            
            </figure>
            <figure className="graphs" id="graph2">
                <Line data={data2} options={options} />           
            </figure>
        </section>
    );
}

export default Graphs;

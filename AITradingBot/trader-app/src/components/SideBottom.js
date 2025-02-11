import axios from "axios";
import React, { useEffect, useState } from "react";

function SideBottom() {
    const [tradeStatus, setTradeStatus] = useState('Stopped');
    const [nextTradeDate, setNextTradeDate] = useState('N/A');
    const [days, setDays] = useState(1);

    useEffect(() => {
        axios.get('http://localhost:5000/get_trade_status')
            .then(response => {
                if (response.status && response.status !== undefined) {
                    setTradeStatus(response.data.status);
                }
            })
            .catch(error => console.error('Error fetching trade status:', error));
    }, []);

    useEffect(() => {
        axios.get('http://localhost:5000/get_next_trade_date')
            .then(response => {
                if (response.data && response.data.next_trade !== undefined) {
                    setNextTradeDate(response.data.next_trade);
                }
            })
            .catch(error => console.error('Error fetching next trade date:', error));
    }, []);

    const handleDaysChange = (event) => {
        setDays(event.target.value);
    };

    const handleStopClick = () => {
        axios.get('http://localhost:5000/stop_trading')
            .then(response => {
                if (response.data.status === 'Success') {
                    console.log('Trade stopped successfully');
                    alert('Trade stopped successfully');
                    setTradeStatus('Stopped');
                    setNextTradeDate('N/A');
                }
            })
            .catch(error => console.error('Error stopping trade:', error));
    };

    const handleContinuousClick = () => {
        if (isNaN(days) || days <= 0) {
            alert('Days must be a valid number greater than 0');
            return;
        }
        axios.post('http://localhost:5000/start_trading', { days: days })
            .then(response => {
                if (response.data.status === 'Success') {
                    console.log('Trade started successfully');
                    alert('Trade started successfully');
    
                    setTimeout(() => {
                        axios.get('http://localhost:5000/get_trade_status')
                            .then(response => {
                                if (response.data && response.data.status !== undefined) {
                                    setTradeStatus(response.data.status);
                                }
                            })
                            .catch(error => console.error('Error fetching trade status:', error));
    
                        axios.get('http://localhost:5000/get_next_trade_date')
                            .then(response => {
                                if (response.data && response.data.next_trade !== undefined) {
                                    setNextTradeDate(response.data.next_trade);
                                }
                            })
                            .catch(error => console.error('Error fetching next trade date:', error));
                    }, 2000);
                }
            })
            .catch(error => console.error('Error starting trade:', error));
    };
    
    

    const getStatusClass = () => {
        switch (tradeStatus) {
            case 'Active':
                return 'status-active';
            case 'Stopped':
                return 'status-stopped';
            default:
                return '';
        }
    };
    
    return (
    <section id="sidebottom">
        <div className="continous-trade-button-container">
            <button id="continous-trade" onClick={handleContinuousClick}>Continous</button>
        </div>
        <div className="days-input-container">
            <p>Days</p>
            <input type="number" id="days-input" value={days} onChange={handleDaysChange}></input>
        </div>
        <div className="status-container">
            <p>Status</p>
            <p id="status" className={getStatusClass()}>{tradeStatus}</p>
        </div>
        <div className="next-trade-date-container">
            <p>Next Trade Date</p>
            <p id="next-trade-date">{nextTradeDate}</p>
        </div>
        <div className="stop-button-container">
            <button id="stop-button" onClick={handleStopClick}>Stop</button>
        </div>
    </section>
    );
}

export default SideBottom;
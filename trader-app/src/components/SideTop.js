import React, { useEffect, useState } from 'react';
import axios from 'axios';

function SideTop() {
    const [assetBalance, setAssetBalance] = useState(0);
    const [accountBalance, setAccountBalance] = useState(0);

    useEffect(() => {
        axios.get('http://localhost:5000/get_asset_balance') 
            .then(response => {
                if (response.data && response.data.asset_balance !== undefined) {
                    setAssetBalance(response.data.asset_balance);
                }
            })
            .catch(error => console.error('Error fetching asset balance:', error));
    }, []);

    useEffect(() => {
        axios.get('http://localhost:5000/get_account_balance') 
            .then(response => {
                if (response.data && response.data.account_balance !== undefined) {
                    setAccountBalance(response.data.account_balance);
                }
            })
            .catch(error => console.error('Error fetching account balance:', error));
    }, []);
    
    
    const handleTradeClick = () => {
        axios.get('http://localhost:5000/auto_trade')
            .then(response => {
                if (response.data === 'Success') {
                    console.log('Trade executed successfully');
                    alert('Trade executed successfully');
            }
            })
            .catch(error => console.error('Error executing trade:', error));
    };
    
    return (
        <section id="sidetop">
            <div className="account-balance-contaier">
                <p>Account Balance</p>
                <p id="account-balance">{accountBalance}</p>         
            </div>
            <div className="asset-balance-container">
                <p>Asset Balance</p>
                <p id="asset-balance">{assetBalance}</p>
            </div>
            <div className="single-trade-button-container">
                <button id="single-trade" onClick={handleTradeClick}>Single Trade</button>
            </div>
        </section>
    );
}

export default SideTop;
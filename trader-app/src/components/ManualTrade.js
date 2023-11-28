import React, {useEffect, useState} from 'react';
import axios from 'axios';

function ManualTrade() {
    const [suggestedAction, setSuggestedAction] = useState('N/A');
    const [buyAmount, setBuyAmount] = useState(1);
    const [sellAmount, setSellAmount] = useState(1);

    useEffect(() => {
        axios.get('http://localhost:5000/get_trade_decision')
            .then(response => {
                if (response.data && response.data.trade_decision !== undefined) {
                    const tradeDecision = response.data.trade_decision;
                    setSuggestedAction(tradeDecision.charAt(0).toUpperCase() + tradeDecision.slice(1));
                }
            })
            .catch(error => console.error('Error fetching suggested action:', error));
    }, []);

    const handleBuyAmountChange = (event) => {
        setBuyAmount(event.target.value);
    }

    const handleSellAmountChange = (event) => {
        setSellAmount(event.target.value);
    }

    const handleBuyClick = () => {
        if (isNaN(buyAmount) || buyAmount <= 0) {
            alert('Buy amount must be a valid number greater than 0');
            return;
        }
        axios.post('http://localhost:5000/buy_trade', { amount: buyAmount })
            .then(response => {
                if (response.data.status === 'Success') {
                    let msg = response.data.message;
                    console.log('Buy executed successfully');
                    alert(msg);
                } else {
                    console.error('Unexpected response:', response.data);
                }
            })
            .catch(error => console.error('Error executing buy:', error));
    };
    

    const handleSellClick = () => {
        if (isNaN(sellAmount) || sellAmount <= 0) {
            alert('Sell amount must be a valid number greater than 0');
            return;
        }
        axios.post('http://localhost:5000/sell_trade' ,{ amount: sellAmount})
            .then(response => {
                if (response.data.status === 'Success') {
                    console.log('Sell executed successfully');
                    alert('Sell executed successfully');
                }
            })
            .catch(error => console.error('Error executing sell:', error));
    };

    const getTradeDec = () => {
        switch (suggestedAction) {
            case 'buy':
                return 'Buy';
            case 'sell':
                return 'Sell';
            case 'hold':
                return 'Hold';
            default:
                return 'N/A';
        }
    };



    return (
        <section className="manualtrade">
        <label id="manuallable">
            <div>Manual Trade</div>
        </label>
        <div id="suggestedaction-container">
            <p>Suggested Action</p>
            <p id="suggestedaction">{suggestedAction}</p>
        </div>
        <div id="manualbuttons">
            <div id="buyamounts">
                <input type="number" id="buy-input" value={buyAmount} onChange={handleBuyAmountChange}></input>
            </div>
            <div id="sellamounts">
                <input type="number" id="sell-input" value={sellAmount} onChange={handleSellAmountChange}></input>
            </div>
            <div id="buy-button-div">
                <button id="buybutton" onClick={handleBuyClick}>Buy</button>
            </div>
            <div id="sell-button-div">
                <button id="sellbutton" onClick={handleSellClick}>Sell</button>
            </div>
        </div>
    </section>
    );
}
  
export default ManualTrade;
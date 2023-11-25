import React, {useEffect, useState} from 'react';
import axios from 'axios';

function ManualTrade() {
    const [suggestedAction, setSuggestedAction] = useState('Buy');
    const [buyAmount, setBuyAmount] = useState(1);
    const [sellAmount, setSellAmount] = useState(1);

    useEffect(() => {
        axios.get('http://localhost:5000/get_trade_decision')
            .then(response => {
                if (response.data && response.data.trade_decision !== undefined) {
                    setSuggestedAction(response.data.trade_decision);
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
        axios.get('http://localhost:5000/buy_trade?amount=' + buyAmount)
            .then(response => {
                if (response.data === 'Success') {
                    console.log('Buy executed successfully');
                    alert('Buy executed successfully');
                }
            })
            .catch(error => console.error('Error executing buy:', error));
    };

    const handleSellClick = () => {
        axios.get('http://localhost:5000/sell_trade?amount=' + sellAmount)
            .then(response => {
                if (response.data === 'Success') {
                    console.log('Sell executed successfully');
                    alert('Sell executed successfully');
                }
            })
            .catch(error => console.error('Error executing sell:', error));
    };

    return (
        <section class="manualtrade">
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
                <button id="buybutton">Buy</button>
            </div>
            <div id="sell-button-div">
                <button id="sellbutton">Sell</button>
            </div>
        </div>
    </section>
    );
}
  
export default ManualTrade;
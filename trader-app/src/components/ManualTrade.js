import React from 'react';

function ManualTrade() {
    return (
        <div className="manualtrade">
            <div id="manuallable">
                <div>Manual Trade</div>
            </div>
            <div id="suggestedaction-container">
                <p>Suggested Action</p>
                <p id="suggestedaction">Buy</p>
            </div>
            <div id="manualbuttons">
                <div id="buyamounts">
                    <input type="number" id="buy-input" value="1"></input>
                </div>
                <div id="sellamounts">
                    <input type="number" id="sell-input" value="1"></input>
                </div>
                <div id="buy-button-div">
                    <button id="buybutton">Buy</button>
                </div>
                <div id="sell-button-div">
                    <button id="sellbutton">Sell</button>
                </div>
            </div>   
        </div>
    );
}
  
export default ManualTrade;
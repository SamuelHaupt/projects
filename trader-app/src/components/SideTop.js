import React from "react";

function SideTop() {
    return (
        <section id="sidetop">
            <div className="account-balance-contaier">
                <p>Account Balance</p>
                <p id="account-balance">0</p>
            </div>
            <div className="asset-balance-container">
                <p>Asset Balance</p>
                <p id="asset-balance">0</p>
            </div>
            <div className="single-trade-button-container">
                <button id="single-trade">Single Trade</button>
            </div>
        </section>
    );
}

export default SideTop;
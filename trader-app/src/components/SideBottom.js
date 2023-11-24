import React from "react";

function SideBottom() {
    return (
        <section id="sidebottom">
            <div className="continous-trade-button-container">
                <button id="continous-trade">Continous</button>
            </div>
            <div className="days-input-container">
                <p>Days</p>
                <input type="number" id="days-input" value="1"></input>
            </div>
            <div className="status-container">
                <p>Status</p>
                <p id="status">Idle</p>
            </div>
            <div cclassNamelass="next-trade-date-container">
                <p>Next Trade Date</p>
                <p id="next-trade-date">N/A</p>
            </div>
            <div className="stop-button-container">
                <button id="stop-button">Stop</button>
            </div>
        </section>
    );
}

export default SideBottom;
import React, {useState, useEffect} from 'react';
import axios from 'axios';

function Info() {
  const [buyingPower, setBuyingPower] = useState(0);
  const [assetPrice, setAssetPrice] = useState(0);
  const [totalValue, setTotalValue] = useState(0);
  const [lastTrade, setLastTrade] = useState(['N/A']);

  useEffect(() => {
    axios.get('http://localhost:5000/get_buying_power')
      .then(response => {
        if (response.data && response.data.buying_power !== undefined) {
          setBuyingPower(response.data.buying_power);
        }
      })
      .catch(error => console.error('Error fetching buying power:', error));
  }, []);

  useEffect(() => {
    axios.get('http://localhost:5000/get_asset_price')
      .then(response => {
        if (response.data && response.data.asset_price !== undefined) {
          setAssetPrice(response.data.asset_price);
        }
      })
      .catch(error => console.error('Error fetching asset price:', error));
  }
  , []);

  useEffect(() => {
    axios.get('http://localhost:5000/get_total_value')
      .then(response => {
        if (response.data && response.data.total_value !== undefined) {
          setTotalValue(response.data.total_value);
        }
      })
      .catch(error => console.error('Error fetching total value:', error));
  }
  , []);

  useEffect(() => {
    axios.get('http://localhost:5000/get_latest_trades')
      .then(response => {
        if (response.data && response.data.latest_trades) {
          const trades = response.data.latest_trades;
          if (Object.keys(trades).length === 0) {
            setLastTrade(['N/A']);
            return;
          }
          const formattedTrades = Object.entries(trades).map(([date, tradeType]) => `${date}: ${tradeType}`);
          setLastTrade(formattedTrades);
        }
      })
      .catch(error => console.error('Error fetching latest_trades:', error));
  }, []);

  const tradeDisplay = lastTrade.join(', ');


  return (
    <section className="info-section">
        <div className="info" id="info1">
            <p>Buying Power</p>
            <p>{buyingPower}</p>
            <p>Asset Price</p>
            <p>{assetPrice}</p>
        </div>
        <div className="info" id="info2">
            <p>Total Portfolio</p>
            <p>{totalValue}</p>
            <p>Latest Trades</p>
            <p>{tradeDisplay}</p>
        </div>
    </section>
  );
}

export default Info;
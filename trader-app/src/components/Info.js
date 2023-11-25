import React, {useState, useEffect} from 'react';

function Info() {
  const [buyingPower, setBuyingPower] = useState(0);
  const [assetPrice, setAssetPrice] = useState(0);
  const [totalValue, setTotalValue] = useState(0);
  const [latestTrades, setlatestTrades] = useState(0);

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
        if (response.data && response.data.last_trade !== undefined) {
          setLastTrade(response.data.latest_trades);
        }
      })
      .catch(error => console.error('Error fetching latest_trades:', error));
  }
  , []);


  return (
    <section class="info-section">
        <div class="info" id="info1">
            <p>Buying Power</p>
            <p>{buyingPower}</p>
            <p>Asset Price</p>
            <p>{assetPrice}</p>
        </div>
        <div class="info" id="info2">
            <p>Total Portfolio</p>
            <p>{totalValue}</p>
            <p>Latest Trades</p>
            <p>{latestTrades}</p>
        </div>
    </section>
  );
}

export default Info;
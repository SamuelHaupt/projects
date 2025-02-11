import React from 'react';
import { Link } from 'react-router-dom';

function Header() {
  return (
    <div>
      <ul>
        <li><a href="/">Trade</a></li>
        <li><h1>TQQ Trader</h1></li>
        <li><Link to="/train">Train</Link></li>
      </ul>
    </div>

  );
}

export default Header;

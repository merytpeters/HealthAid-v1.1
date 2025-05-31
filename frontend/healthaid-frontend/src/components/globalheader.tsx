import { useState } from 'react';
import '../styles/globalheader.css';

function GlobalHeader() {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <nav className="global-header">
      <div className="nav-container">

        <button
          className="menu-toggle"
          onClick={() => setMenuOpen(!menuOpen)}
          aria-label="Toggle menu"
        >
          ☰
        </button>

        <ul className={`nav-list ${menuOpen ? 'open' : ''}`}>
          <li><a href="/#features">Features</a></li>
          <li><a href="/">Pricing</a></li>
          <li><a href="/">Contact</a></li>
          <li><a href="/">Signup</a></li>
          <li><a href="/">About</a></li>
        </ul>
      </div>
    </nav>
  );
}

export default GlobalHeader;

import './Header.css'
import { Globe } from './components'


function Header() {
  return (
    <div className="Header">
      <div className="Header-Textarea">
        <div className="Header-Text">
          <h1>
            CITIES
          </h1>
          <p>
            Buy, hold and trade cities. Earn ERC-721 achievement tokens and climb the Leaderboard.
          </p>
        </div>
        <div className="Header-Navigation">
          <nav>
            <a>Home</a>
            <a>Inventory</a>
            <a>Leaderboard</a>
          </nav>
          <button>Connect Wallet</button>
        </div>
      </div>
      <div className="Header-GlobePadding">
        <div className="Header-GlobeAspectRatioControl">
          <div>
            <Globe />
          </div>
        </div>
      </div>
    </div>
  )
}

export default Header

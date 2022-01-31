import './Header.css'
import { Globe, AspectRatioControl, Navigation } from '..'


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
          <Navigation />
          <button>Connect Wallet</button>
        </div>
      </div>
      <div className="Header-GlobePadding">
        <AspectRatioControl>
          <Globe />
        </AspectRatioControl>
      </div>
    </div>
  )
}

export default Header

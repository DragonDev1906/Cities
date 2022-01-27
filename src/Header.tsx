import './Header.css'
import Globe from './Globe'


function Header() {
  return (
    <div className="Header">
      <div className="Header-Text">
        <h1>
          CITIES
        </h1>
        <p>
          Buy, hold and trade cities. Earn ERC-721 achievement tokens and climb the Leaderboard.
        </p>
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

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
        <Navigation />
      </div>
      <div className="Header-Globe">
        <AspectRatioControl>
          <Globe />
        </AspectRatioControl>
      </div>
    </div>
  )
}

export default Header

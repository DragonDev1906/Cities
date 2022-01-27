import './App.css'
import Globe from './Globe'


function App() {
  return (
    <div className="App">
      <div className="App-Header">
        <h1>
          CITIES
        </h1>
        <p>
          Buy, hold and trade cities. Earn ERC-721 achievement tokens and climb the Leaderboard.
        </p>
      </div>
      <div className="App-GlobePadding">
        <div className="App-GlobeAspectRatioControl">
          <div>
            <Globe />
          </div>
        </div>
      </div>
    </div>
  )
}

export default App

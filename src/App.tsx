import './App.css'
import Globe from './Globe'


function App() {
  return (
    <div className="App">
      <h1 className="App-Title">
        Cities
      </h1>
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

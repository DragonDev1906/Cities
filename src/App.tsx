import './App.css'
import { Header, ActivityLog } from './components'
import { getPriorityConnector, initializeConnector } from '@web3-react/core'
import { MetaMask } from '@web3-react/metamask'

const [metaMask, metaMaskHooks] = initializeConnector<MetaMask>((actions) => new MetaMask(actions))
const { usePriorityConnector } = getPriorityConnector(
  [metaMask, metaMaskHooks]
)

function App() {
  const priorityConnector = usePriorityConnector()

  return (
    <div className="App">
      <Header />
      <ActivityLog />
    </div>
  )
}

export default App

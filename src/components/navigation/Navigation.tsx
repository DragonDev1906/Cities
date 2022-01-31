import './Navigation.css'

function Navigation() {
  return (
    <div className="Navigation-Container">
      <nav className="Navigation">
        <a>Home</a>
        <a>Inventory</a>
        <a>Achievements</a>
        <a>Leaderboard</a>
      </nav>
      <button className='Navigation-ConnectWallet'>
        Connect Wallet
      </button>
    </div>

  )
}

export default Navigation

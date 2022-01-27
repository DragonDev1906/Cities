import './Header.css'
import Globe from './Globe'


function Header() {
  return (
    <div className="ActivityLog">
        {/* Log types: */}
        {/* 1) City <name> transfered from <addr> to <addr> */}
        {/* 2) City <name> sold on <platform> to <addr> for <amt> */}
        {/* 3) City <name> minted by <addr> for <amt> */}
        {/* 4) <amt> claimed by <addr> */}
        {/* 5) Achievement <name> can be claimed by <addr> */}
        {/* 6) Achievement <name> claimed by <addr> */}
        {/* 7) <addr> reached <place> on the leaderboard */}
        {/* 8) City <name> leveled up to <level> */}
    </div>
  )
}

export default Header

import './Header.css'
import Globe from './Globe'


function Header() {
  return (
    <div className="ActivityLog">
        {/* 
            Filters:
            - Claims
            - Transfers
            - Sales
            - Leaderboard
            - Levelups
            - OnlyMyActivity
            types:
            - City <name> minted by <addr> for <amt>
            - City <name> transfered from <addr> to <addr>
            - City <name> added to <platform> for <amt>
            - City <name> sold on <platform> to <addr> for <amt>
            - Achievement <name> can be claimed by <addr>
            - Achievement <name> claimed by <addr>
            - Achievement <name> transfered from <addr> to <addr>
            - Achievement <name> added to <platform> for <amt>
            - Achievement <name> sold on <platform> to <addr> for <amt>
            - <addr> reached <place> on the leaderboard
            - City <name> leveled up to <level> 
            - <amt> influence claimed by <addr>
        */}
    </div>
  )
}

export default Header

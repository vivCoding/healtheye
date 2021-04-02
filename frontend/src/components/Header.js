import { Icon } from '@iconify/react'
import locationIcon from '@iconify/icons-mdi/social-distance-2-meters'
const Header = () => {
    return (
        <header className="header">
            <h1><Icon icon={locationIcon} /> Social Distancing Tracker</h1>
        </header>
    )
}

export default Header
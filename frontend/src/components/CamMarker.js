import { Icon } from '@iconify/react'
import locationIcon from '@iconify/icons-mdi/camera-gopro'

const CamMarker = ({ lat, lng }) => {
    return (
        <div className="location-marker">
            <Icon icon={locationIcon} className="location-icon" />
        </div>
    )
}

export default CamMarker
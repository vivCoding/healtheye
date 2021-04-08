import React, { useState,  useEffect } from 'react'
import { Map, InfoWindow, Marker, GoogleApiWrapper } from 'google-maps-react';

const MapContainer = ({updateFunction, entries, google}) => {

    return (
        <Map
            google = {google}
            zoom={14}
            containerStyle={{ maxWidth: "80%", height: "80%", position:"relative" }}
            style={{
                width: '700px', height: '700px',
            }}
            initialCenter={{
                lat: 40.4237,
                lng: -86.9212
            }}
        >
            {entries.map(entry => (
                <Marker
                    name = {entry.location.name}
                    position = {entry.coordinates}
                    onClick = {() => {
                        updateFunction(entry);
                    }}
                />
            ))}
        </Map>
    )
}

export default GoogleApiWrapper({
  apiKey: ('AIzaSyC3RmyXyx5rURrCYvF5RNOa8GJ8DfsFFMA')
})(MapContainer)
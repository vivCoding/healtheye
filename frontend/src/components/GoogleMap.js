import React, { Component} from 'react';
import {Map, InfoWindow, Marker, GoogleApiWrapper} from 'google-maps-react';

export class MapContainer extends Component {
    constructor(props) {
        super(props);
    
        this.state = {
          attractions: [{latitude: 40.427790, longitude: -86.916960}, // Lawson
                  {latitude: 40.428313, longitude: -86.922457}, //Co rec sports center
                  {latitude: 40.424995, longitude: -86.915833}, //Founders Park
                  {latitude: 40.434460, longitude: -86.918449} //Ross Ade Stadium
                  ]
        }
      }

    state = {
      showingInfoWindow: false,
      activeMarker: {},
      selectedPlace: {},
    };

   
    onMarkerClick = (props, marker, e) =>
      this.setState({
        selectedPlace: props,
        activeMarker: marker,
        showingInfoWindow: true
      });
   
    onMapClicked = (props) => {
      if (this.state.showingInfoWindow) {
        this.setState({
          showingInfoWindow: false,
          activeMarker: null
        })
      }
    };

    displayMarkers = () => {
        return this.state.attractions.map((attractions, index) => {
          return <Marker key={index} id={index} position={{
           lat: attractions.latitude,
           lng: attractions.longitude
         }}
         />
        })
      }
   
    render() {
      return (
        <Map google={this.props.google}
            containerStyle={{ maxWidth: "700px", height: "550px" }}
            style={{width: '100%', height: '100%', position: 'relative'}}
            
            initialCenter={{
                lat: 40.4237,
                lng: -86.9212
            }}
            zoom={14}
            onClick={this.onMapClicked}>
          
          {this.displayMarkers()}        
        </Map>
      )
    }
  }

  export default GoogleApiWrapper({
    apiKey: ('AIzaSyC3RmyXyx5rURrCYvF5RNOa8GJ8DfsFFMA')
  })(MapContainer)

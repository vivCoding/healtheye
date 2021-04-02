import React, { Component} from 'react';
import CamMarker from './CamMarker'
import {Map, InfoWindow, Marker, GoogleApiWrapper} from 'google-maps-react';



export class MapContainer extends Component {
    constructor(props) {
        super(props);
       
        this.state = {
          showingInfoWindow: false,
          activeMarker: {},
          selectedPlace: {},
          attractions: [{latitude: 40.427790, longitude: -86.916960}, // Lawson
                  {latitude: 40.428313, longitude: -86.922457}, //Co rec sports center
                  {latitude: 40.424995, longitude: -86.915833}, //Founders Park
                  {latitude: 40.434460, longitude: -86.918449} //Ross Ade Stadium
                  ]
        }
        
      }
/*
    state = {
      showingInfoWindow: false,
      activeMarker: {},
      selectedPlace: {},
    };

    */

   
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
        
            containerStyle={{ maxWidth: "50%", height: "80%" }}
            style={{width: '100%', height: '100%', position: 'relative'}}

            initialCenter={{
                lat: 40.4237,
                lng: -86.9212
            }}
            zoom={14}
            onClick={this.onMapClicked}>
            
            <Marker
              onClick={this.onMarkerClick}
              name={'Walc'}
              position={{lat: 40.4274, lng: -86.9132}}
              danger ={'Very Danger'}
            />
            <InfoWindow
              marker={this.state.activeMarker}
              visible={this.state.showingInfoWindow}
              onClose={this.onClose}
              className="walc"
            >
              <div>
                <h4>{this.state.selectedPlace.name}</h4>
                <h5>{this.state.selectedPlace.danger}</h5>
              </div>
            </InfoWindow>

            <Marker
              onClick={this.onMarkerClick}
              name={'Stewart Center'}
              position={{lat: 40.4250, lng: -86.9126}}
              danger ={'Safe'}
            />
            <InfoWindow
              marker={this.state.activeMarker}
              visible={this.state.showingInfoWindow}
              onClose={this.onClose}
            >
              <div>
                <h4>{this.state.selectedPlace.name}</h4>
                <h5 className = 'corec'>{this.state.selectedPlace.danger}</h5>
              </div>
            </InfoWindow>

            <Marker
              onClick={this.onMarkerClick}
              name={'Hillenbrand Lounge'}
              position={{lat: 40.4269, lng: -86.9264}}
              danger ={'Safe'}
            />
            
            <InfoWindow 
              
              marker={this.state.activeMarker}
              visible={this.state.showingInfoWindow}
              onClose={this.onClose}
            >
              <div>
                <h4>{this.state.selectedPlace.name}</h4>
                <h5 className = 'founders'>{this.state.selectedPlace.danger}</h5>
              </div>
            </InfoWindow>
            
            
        

         
          
        </Map>
      )
    }
  }

  export default GoogleApiWrapper({
    apiKey: ('AIzaSyC3RmyXyx5rURrCYvF5RNOa8GJ8DfsFFMA')
  })(MapContainer)

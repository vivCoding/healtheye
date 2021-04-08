import "./App.css"
import React, { useState, useEffect } from 'react'

import GoogleMap from "./components/GoogleMap"

const App = () => {

    const [entries, setEntries] = useState([])

    const [newTime, setNewTime] = useState("")
    const [newDate, setNewDate] = useState("")

    const [current, setCurrent] = useState({
        time: new Date().toISOString().slice(0, 10),
        date: new Date().toISOString().slice(11, 19)
    })

    const getData = (pdate, ptime) => {
        let date = pdate || new Date().toISOString().slice(0, 10);
        let time = ptime || new Date().toISOString().slice(11, 19);
        setCurrent({
            time: time,
            date: date
        });
        console.log("nfwefwef");
        fetch("https://covid-db-access.azurewebsites.net/api/getentryfromtime?" + new URLSearchParams({
            time: date + " " + time
        })).then(response => {
            return response.json();
        }).then(data => {
            console.log("nice");
            let newData = data.map(entry => {
                return {...entry, coordinates: {
                    lat: parseFloat(entry.location.latitude),
                    lng: parseFloat(entry.location.longitude)
                }}
            })
            setEntries(newData);
        }).catch(error => {
            console.log("error!", error)
        })
        
    }

    useEffect(() => {
        getData();
    }, [])

    const [dataToShow, updateData] = useState({});

    const handleUpdateData = (entry) => {
        updateData(entry);
    }

    return (
        <div id="container">
            <h1 id = "title">HealthEye</h1>
            <div id = "dashboard">
                <div class= "stats">
                    <h1>General Information</h1>
                    <ul>
                        <li>People Count: {dataToShow.people || 0} </li>
                        <li>Social distance violations: {dataToShow.violations || 0}</li>
                        <li>Location Name: {dataToShow.location ? dataToShow.location.name : "none specified"}</li>
                    </ul>
                    <p>Showing {current.time} on {current.date}</p>
                    <h3>Choose a date:</h3>
                    <p>Enter in yyyy-mm-dd format</p>
                    <input placeholder = {current.date} value = {newDate} onChange = {e => {
                        setNewDate(e.target.value);
                    }}/>
                    <h3>Choose a time:</h3>
                    <p>Enter in hh:mm:ss format</p>
                    <input placeholder = {current.time} value = {newTime} onChange = {e => {
                        setNewTime(e.target.value);
                    }}/>
                    <br></br>
                    <br></br>
                    <button onClick = {() => {
                        getData(newDate, newTime);
                    }}>Refresh</button>
                    <h4>Note: work in progress</h4>
                    <p>Some test values</p>
                    <ul id = "note">
                        <li>Date: 2021-04-01</li>
                        <li>Time: 12:01:21 up to 12:50:21</li>
                    </ul>
                </div>
                <div>
                    <GoogleMap updateFunction = {handleUpdateData} entries = {entries}/>
                </div>
            </div>
        </div>
    )
}

export default App;


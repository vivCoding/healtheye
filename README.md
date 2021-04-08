# HealthEye

Submission to the [Microsoft Azure AI Hackathon 2021](https://devpost.com/software/healtheye)

## What it does
HealthEye is an IoT system that allows you to monitor the number of people and social distancing violations in a certain area. It uses a Raspberry Pi and camera system to analyze the number of people and the number of social distancing violations for a specific area. Additionally, it is able to forecast the number of people and social distancing violations for a future time that a user can select.

As proof of concept, we also included the ability for the system to input video files as well as camera feed.

## How we built it
![current_architecture](https://raw.githubusercontent.com/vivCoding/healtheye/main/docs/current_architecture.png)

### Computer Vision
We utilized [Azure Custom Vision API](https://docs.microsoft.com/en-us/azure/cognitive-services/custom-vision-service/) to detect people and their location in a video frame. We decided to use the Custom Vision AI rather than the [Object Detection API](https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/concept-object-detection) as we wanted to train our model on a diverse data set consisting of images of libraries, classrooms, and outdoor scenery.

### Social Distance Calculations
In addition to the Custom Vision model, we used the [CV2](https://docs.opencv.org/master/d6/d00/tutorial_py_root.html) library to help us estimate the true distance between people given the bounding boxes from the vision model. We used image transformations to help us do so

### Web
We used [CosmosDB](https://docs.microsoft.com/en-us/azure/cosmos-db/introduction) to store our data, and used [Azure Functions](https://docs.microsoft.com/en-us/azure/azure-functions/functions-overview) to abstract the code to write/read from the CosmosDB instance. For the final website, we created it using Python Flask and ReactJS, and deployed as a [Azure Web App](https://docs.microsoft.com/en-us/azure/app-service/overview)

### Time Series Prediction (in progress):
We utilized a multivariate time series model (VAR) to predict the number of individuals in a given location and the number of socially distanced violations for a distance threshold that a user could specify. We used data extracted from the CosmosDB database containing the same metrics, extracted from video frames.

## What's next for HealthEye

### Architecture Modification
Our originally planned architecture consisted of this:
![planned_architecture](https://raw.githubusercontent.com/vivCoding/healtheye/main/docs/planned_architecture.png)

We envisioned this solution to be scalable and modular, where it was easy to add a new Raspberry Pi (or any new device) to the system and add more data. [Azure IoT Hub](https://docs.microsoft.com/en-us/azure/iot-hub/about-iot-hub) and [IoT Edge](https://docs.microsoft.com/en-us/azure/iot-edge/about-iot-edge?view=iotedge-2018-06) offered this type of scalability, and thus we wanted to utilize it to its max potential. After failure to properly install IoT Edge on the Raspberry Pi 4 correctly, we set it as a project for the future (after the hackathon demo). However, we still plan to use it to make this entire thing much more scalable and modular.

### Custom Vision
We hope to refine our Azure CV model to be more accurate and more accepting of a wider dataset.

### Web
We'd like to improve the user experience on the website, as most of our work revolved around the backend, thus resulting in an awkward-to-use interface. We know that if this was going into production, the design and UX would have to drastically improve.



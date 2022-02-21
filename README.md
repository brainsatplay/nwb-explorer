# NWB Explorer

NWB Explorer is a web application that can be used by scientists to read, visualize and explore the content of NWB:N 2 files.

> Note: This is a stripped down version of the NWB Explorer that works without a backend using **WebNWB**! See the original version [here](https://github.com/MetaCell/nwb-explorer).

Learn more about the [Neurodata Without Borders](https://www.nwb.org/) data standard.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Below you will find the software you need to install to use nwb explorer (and the versions we used):

* Node (10+) and npm (6+).

## Building the Application
To install all the project dependencies, run:
```bash
npm install
```

To activate the Webpack development server, run:
```bash
npm run build-dev-noTest:watch
```

This will spawn a process that while left running will watch for any changes on the `src` folder and automatically deploy them each time a file is saved.

To begin interfacing with NWB Explorer, spawn a second terminal and run: 
```bash
npm start
```

If everything worked, the default browser will open on `http://localhost:8081/build/geppetto.html`.

## Getting started with NWB Explorer

When the application is started, no file will be loaded.

1. Use the interface to load the file from a public url or just load a sample
1. Specify the parameter nwbfile in your browser. Example: `http://localhost:8081/build/geppetto.html?nwbfile=https://github.com/OpenSourceBrain/NWBShowcase/raw/master/NWB/time_series_data.nwb`

## Built With

* [Geppetto](http://www.geppetto.org/) - Used to build a web-based application to interpret and visualize the NWB:N 2 files.
* [WebNWB](https://github.com/brainsatplay/webnwb) - Used to read and manipulate NWB:N 2 files

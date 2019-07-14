# Introduction

A set of Google Cloud services used to generate tiled video maps.

# Usage

... TODO
                       
# Changelog

## 2019-07-15

Implemented a skeleton using Google Cloud Functions and a Firebase as a database to manage video export tasks.

For developers, check the following to get a new record (video map export) added to the database:

https://us-central1-deltares-video-map.cloudfunctions.net/exportVideoMapTiles?name=blablabla



# Development
    
Use the following command to deploy cloud functions:

`npm run deploy`


The following tools are used:

* Google Cloud Functions

* Firebase to keep real-time database of current video map export tasks

https://firebase.google.com/docs/functions/get-started


               

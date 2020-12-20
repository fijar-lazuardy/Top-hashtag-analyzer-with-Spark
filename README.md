# pdb-7-spark-streaming

A repository for Big Data Management course final project

## About

This is an app that can find top 10 hashtags of Musician related tweets that are tweeted in Bahasa. Using Twitter API V2 to stream the tweets, spark app to process the tweets, MongoDB to save the data, and flask to display the top 10 hashtags tweeted.

## Workflow

First, there's a python script that will stream tweets using Twitter API v2 and send all the data streamed using socket.  
A Spark app that is submitted before will iterate all tweets received from socket and process it. After the data is processed, it will send those data to MongoDB, and then it will be displayed on dashboard

## Pre-requisites

- Docker
- dokcer-compose

## Run the app

Change .env.example and rename it as .env  
Fill all the fields with your credentials.  
  
Then run this command

```bash
dokcer-compose up
```

To start the cluster and your tweet stream script

Build and run image on ```apache-stream``` folder, make sure to change the IP on the script to IP from tweet-streamer container, use same network as the spark cluster and adjust your mongoDB Uri.  

Run the flask app

## Stack

This repository contain a standalone spark cluster taken from [here](https://github.com/big-data-europe/docker-spark)

This app consist 1 Master Node & 2 Worker node

- Apache Spark
- Python (to stream tweets)
- Spark app (to process the tweets)
- Mongo DB (to save the tweets)
- Flask (for dashboard)

### Big shoutout for Big-Data-Europe for their amazing jobs! Check their works on github [here](https://github.com/big-data-europe/) and all their docker images from [here](https://hub.docker.com/u/bde2020)
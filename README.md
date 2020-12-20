# pdb-7-spark-streaming
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-2-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

A repository for Big Data Management course final project

## About

This is an app that can find top 10 hashtags of Musician related tweets that are tweeted in Bahasa. Using Twitter API V2 to stream the tweets, spark app to process the tweets, MongoDB to save the data, and flask to display the top 10 hashtags tweeted.

## Workflow

First, there's a python script that will stream tweets using Twitter API v2 and send all the data streamed using socket.  
A Spark app that is submitted before will iterate all tweets received from socket and process it. After the data is processed, it will send those data to MongoDB, and then it will be displayed on dashboard

## Pre-requisites

- Docker
- dokcer-compose
- A running MongoDB instance

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
## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/fijar-lazuardy"><img src="https://avatars0.githubusercontent.com/u/32705957?v=4" width="100px;" alt=""/><br /><sub><b>Fijar Lazuardy</b></sub></a><br /><a href="#infra-fijar-lazuardy" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="https://github.com/fijar-lazuardy/pdb-7-spark-streaming/commits?author=fijar-lazuardy" title="Code">💻</a></td>
    <td align="center"><a href="http://razrinn.com"><img src="https://avatars1.githubusercontent.com/u/47453890?v=4" width="100px;" alt=""/><br /><sub><b>Ray Azrin Karim</b></sub></a><br /><a href="https://github.com/fijar-lazuardy/pdb-7-spark-streaming/commits?author=razrinn" title="Code">💻</a></td>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
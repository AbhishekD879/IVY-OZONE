### What is this repository for? ###
* This repository contains source code of surface-bets reactions microservice.
### Architecture:
![Scheme](surfacebets.PNG)

### Functionality:
* Once the user logged-in Emojis will be pulled from CMS asset management.
* Once the user opted one of the Emojis, API call will be initiated to Reactions MS.
* Data will be pushed into Redis (i.e., Producer). Other users opted count will be published into Redis streams using API call.
* Aggregated counts (i.e., LIKES_COUNT, DISLIKES_COUNT, SURPRISE_COUNT) and User specific information will be stored into Redis.
* Reactions MS will save the aggregated and user specific data into Mongo DB for data retention.
* Emojis configuration changes will be pushed into cloudflare changes Kafka Listener (Push Mechanism).

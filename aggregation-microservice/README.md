```
Application for aggregating images of silks into sprites
```

**How to run:**
```
... make sure redis is available ...
./gradlew bootRun
```

or

```
./gradlew build dockerBuildImage
docker-compose up
```

```
... Need to set the below VM variables in order to route through the proxy ...
http.proxyHost={host name}
http.proxyPort={port number}
```

## This service consume Live updates from LiveServ through long-pooling and publish received messages to Hazlcast topics based on channel name. ##


Technologies:

* Java 8
* Spring / Spring Boot

Building


```
#!console

gradle clean build
```


Run integration tests

```
#!console

SPRING_PROFILES_ACTIVE=integration-test gradle clean integrationTest --stacktrace --debug
```

## Endpoints for building / deployment / kibana ##
[https://confluence.egalacoral.com/display/SPI/Endpoints](Link URL)

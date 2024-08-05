Java SDK Client API for Live Server
-------------------
This project provides Java API for [Live Server](https://confluence.egalacoral.com/display/SPI/OpenBet+LiveServe)

#### Prerequisites**

* [Java 8](http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html) installed

* [Gradle >=2.8](http://gradle.org/gradle-download/) installed/configured locally

#### How to build

  gradle clean build

#### How to use

  LiveServerClient client =
        new LiveServerClient("https://push-tst2.coral.co.uk/push", new LiveServerListener() {
          @Override
          public void onMessage(Message message) {
            // handle message
          }
          @Override
          public void onError(Throwable e) {
            // handle error
          }
        });
    client.subscribeOnEvent("2344");
    client.subscribeOnClock("45555");
    client.subscribeOnScore("345345");
    client.connect();


#### Tracer application
This application traces all interaction with Live server to console.

Steps to trace simple event :

 1) Go to https://invictus.coral.co.uk/#/?tab=InPlay <br>
 2) Find {event id} </br>
 3) Run this application with parameter --event.ids={event id}

    java -jar  liveserver-api-1.0.0.jar --event.ids={event id}

 4) Change event https://ss-tst2.coral.co.uk/ti/hierarchy/event/{eventId} <br>
 5) Check output in console

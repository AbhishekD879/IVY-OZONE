**SiteServer Api: Example**

```java
final SiteServerApi siteServerApi = new SiteServerApi.Builder("http://backoffice-tst2.coral.co.uk/")
        .setLoggingLevel(SiteServerAPI.Level.BODY)
        .setConnectionTimeout(1)
        .setReadTimeout(1)
        .setMaxNumberOfRetries(1)
        .setVersion("2.9")
        .build();

final SimpleFilter simpleFilter = new SimpleFilter.SimpleFilterBuilder()
        .addBinaryOperation("event.startTime", BinaryOperation.greaterThanOrEqual, DateTime.now())
        .addBinaryOperation("event.startTime", BinaryOperation.lessThan, DateTime.now().plusDays(1))
        .build();

Optional<List<Event>> events = siteServerApi.getEventForType("1868", simpleFilter);

```

**How to deploy new version to nexus**

* Make sure you have nexus credentials in ~/.gradle/gradle.properties:
```groovy
nexusUser=example
nexusPass=example
```
Actual credentials can be found [here](https://confluence.egalacoral.com/display/SPI/Symphony+Infrastructure+creds#SymphonyInfrastructurecreds-NexusMaven-NPMRegistry).

* Run gradle task to upload artifacts to nexus:
```bash
gradle uploadArchives
- or -
gradle uA
```
Notice that jar artifact will be deployed either to releases or snapshots resository depending on version in build.gradle

Need to set the below VM variables in order to route through the proxy.
http.proxyHost={host name}
http.proxyPort={port number}

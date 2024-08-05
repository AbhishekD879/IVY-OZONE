package com.egalacoral.spark.siteserver.api;

import static org.junit.Assert.assertNotNull;
import static org.mockserver.model.HttpRequest.request;
import static org.mockserver.model.HttpResponse.response;

import com.egalacoral.spark.siteserver.model.Event;
import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.List;
import java.util.stream.Collectors;
import org.junit.Test;
import org.mockserver.client.MockServerClient;
import org.mockserver.integration.ClientAndServer;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import reactor.core.publisher.Mono;
import reactor.test.StepVerifier;

public class SiteServerAsyncImplTest {
  private Integer port = 8443;
  private SiteServerApiAsync siteServerApiAsync =
      new SiteServerAsyncImpl("http://127.0.0.1:8443", "2.31", null, 16777216);
  private final String basePath = "/openbet-ssviewer/Drilldown/2.31/Event";

  @Test
  public void getEventsTest() {
    MockServerClient mockServer = ClientAndServer.startClientAndServer(port);
    try {
      mockServer
          .when(
              request()
                  .withMethod(HttpMethod.GET.name())
                  .withPath(basePath)
                  .withQueryStringParameter("translationLang", "en")
                  .withQueryStringParameter("includeUndisplayed", "true")
                  .withQueryStringParameter("simpleFilter", "event.id:equals:2119676"))
          .respond(
              response()
                  .withStatusCode(HttpStatus.OK.value())
                  .withHeader("Content-Type", "application/json")
                  .withBody(this.getResourceFileAsString("response/getEventForCategory.json")));

      final SimpleFilter simpleFilter =
          (SimpleFilter)
              new SimpleFilter.SimpleFilterBuilder()
                  .addBinaryOperation("event.id", BinaryOperation.equals, 2119676)
                  .build();

      Mono<List<Event>> events = siteServerApiAsync.getEvents(simpleFilter);
      StepVerifier.create(events)
          .assertNext(
              val -> {
                assertNotNull(val);
              })
          .expectComplete()
          .verify();
    } finally {
      mockServer.stop();
    }
  }

  protected String getResourceFileAsString(String resourceFileName) {
    InputStream is = getClass().getClassLoader().getResourceAsStream(resourceFileName);
    BufferedReader reader = new BufferedReader(new InputStreamReader(is));
    return reader.lines().collect(Collectors.joining("\n"));
  }
}

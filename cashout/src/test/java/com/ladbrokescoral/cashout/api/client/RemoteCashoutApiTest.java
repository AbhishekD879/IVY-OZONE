package com.ladbrokescoral.cashout.api.client;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.mockserver.model.HttpRequest.request;
import static org.mockserver.model.HttpResponse.response;

import com.ladbrokescoral.cashout.api.client.entity.request.CashoutRequest;
import com.ladbrokescoral.cashout.api.client.entity.response.CashoutOffer;
import com.ladbrokescoral.cashout.config.WebClientConfig;
import java.net.URISyntaxException;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockserver.client.MockServerClient;
import org.mockserver.integration.ClientAndServer;
import org.mockserver.model.HttpRequest;
import org.mockserver.model.HttpResponse;
import org.mockserver.verify.VerificationTimes;
import org.springframework.http.client.reactive.ReactorResourceFactory;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Flux;
import reactor.test.StepVerifier;

class RemoteCashoutApiTest {

  private Integer port = 8099;
  private String host = "localhost";

  RemoteCashoutApi remoteCashoutApi;

  @BeforeEach
  public void setUp() throws URISyntaxException {
    WebClientConfig conf = new WebClientConfig();
    ReactorResourceFactory resourceFactory = new ReactorResourceFactory();
    resourceFactory.afterPropertiesSet();
    WebClient webclient = conf.cashoutWebClient(host + ":" + port, 100, 100, 10, 100);
    remoteCashoutApi = new RemoteCashoutApiImpl(host + ":" + port, 3, 100, webclient);
  }

  @Test
  void openBetCashoutApiRespondedSuccessfuly() {
    MockServerClient mockServer = ClientAndServer.startClientAndServer(port);

    try {
      mockServer
          .when(request().withMethod("POST").withPath("/").withBody("{}"))
          .respond(
              response()
                  .withStatusCode(200)
                  .withHeader("Content-Type", "application/json")
                  .withBody(
                      "{\n"
                          + "  \"respStatus\": \"SUCCESS\",\n"
                          + "  \"timeStamp\": \"2019-01-23 20:36:22\",\n"
                          + "  \"cashoutOffers\": [\n"
                          + "    {\n"
                          + "      \"cashoutOfferReqRef\": \"1\",\n"
                          + "      \"status\": \"SUCCESS\",\n"
                          + "      \"cashoutValue\": 2.85\n"
                          + "    }\n"
                          + "  ]\n"
                          + "}"));

      Flux<CashoutOffer> cashoutOffers =
          remoteCashoutApi.getCashoutOffers(CashoutRequest.builder().build());
      StepVerifier.create(cashoutOffers)
          .assertNext(
              cashoutOffer -> {
                assertEquals("1", cashoutOffer.getCashoutOfferReqRef());
                assertEquals("SUCCESS", cashoutOffer.getStatus());
                assertEquals((Double) 2.85, cashoutOffer.getCashoutValue());
                assertNull(cashoutOffer.getMessage());
              })
          .expectComplete()
          .verify();
    } finally {
      mockServer.stop();
    }
  }

  @Test
  void openBetCashoutApiRespondedWithNot2xx() {
    MockServerClient mockServer = ClientAndServer.startClientAndServer(port);
    try {
      mockServer
          .when(request().withMethod("POST").withPath("/").withBody("{}"))
          .respond(response().withStatusCode(500).withBody("{}"));

      Flux<CashoutOffer> cashoutOffers =
          remoteCashoutApi.getCashoutOffers(CashoutRequest.builder().build());
      StepVerifier.create(cashoutOffers)
          .assertNext(
              cashoutOffer -> {
                assertEquals(
                    "OPEN_BET_CASHOUT_SERVICE_FAILED_RESPONSE_ERROR", cashoutOffer.getStatus());
                assertNull(cashoutOffer.getCashoutValue());
                assertNull(cashoutOffer.getMessage());
              })
          .expectComplete()
          .verify();
    } finally {
      mockServer.stop();
    }
  }

  @Test
  void expectNoRetriesOnReadTimeout() {
    HttpRequest req = request().withMethod("POST").withPath("/").withBody("{}");
    MockServerClient mockServer = ClientAndServer.startClientAndServer(port);
    try {
      mockServer
          .when(req)
          .respond(
              httpRequest -> {
                try {
                  Thread.sleep(1_100);
                } catch (InterruptedException e) {
                  e.printStackTrace();
                }
                return HttpResponse.response().withStatusCode(200);
              });

      Flux<CashoutOffer> cashoutOffers =
          remoteCashoutApi.getCashoutOffers(CashoutRequest.builder().build());

      StepVerifier.create(cashoutOffers).expectError(RuntimeException.class).verify();

      mockServer.verify(req, VerificationTimes.atLeast(1));
    } finally {
      mockServer.stop();
    }
  }

  @Test
  void openBetCashoutApiRespondedWithError() {
    MockServerClient mockServer = ClientAndServer.startClientAndServer(port);
    try {
      mockServer
          .when(request().withMethod("POST").withPath("/").withBody("{}"))
          .respond(
              response()
                  .withStatusCode(200)
                  .withHeader("Content-Type", "application/json")
                  .withBody(
                      "{"
                          + "  \"respStatus\": \"ERROR\","
                          + "  \"timeStamp\": \"2018-12-27 14:34:26\","
                          + "  \"message\": \"Some error occurred during cashout processing\""
                          + "}"));

      Flux<CashoutOffer> cashoutOffers =
          remoteCashoutApi.getCashoutOffers(CashoutRequest.builder().build());
      StepVerifier.create(cashoutOffers)
          .assertNext(
              cashoutOffer -> {
                assertEquals(
                    "OPEN_BET_CASHOUT_SERVICE_FAILED_RESPONSE_ERROR", cashoutOffer.getStatus());
                assertNull(cashoutOffer.getCashoutValue());
                assertNull(cashoutOffer.getMessage());
              })
          .expectComplete()
          .verify();
    } finally {
      mockServer.stop();
    }
  }
}

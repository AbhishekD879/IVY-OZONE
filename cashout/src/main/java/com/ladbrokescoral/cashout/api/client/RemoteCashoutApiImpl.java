package com.ladbrokescoral.cashout.api.client;

import static com.ladbrokescoral.cashout.model.Code.OPEN_BET_CASHOUT_SERVICE_FAILED_RESPONSE_ERROR;

import com.ladbrokescoral.cashout.api.client.entity.request.CashoutRequest;
import com.ladbrokescoral.cashout.api.client.entity.response.CashoutOffer;
import com.ladbrokescoral.cashout.api.client.entity.response.CashoutOfferResponse;
import com.ladbrokescoral.cashout.util.JsonUtil;
import com.ladbrokescoral.cashout.util.Message;
import com.newrelic.api.agent.ExternalParameters;
import com.newrelic.api.agent.HttpParameters;
import com.newrelic.api.agent.NewRelic;
import com.newrelic.api.agent.Token;
import com.newrelic.api.agent.Trace;
import io.netty.handler.timeout.ReadTimeoutException;
import java.net.URI;
import java.net.URISyntaxException;
import java.text.MessageFormat;
import java.time.Duration;
import java.util.Collections;
import java.util.List;
import java.util.Objects;
import java.util.function.Function;
import org.apache.commons.lang3.tuple.Pair;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.reactivestreams.Publisher;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.BodyInserters;
import org.springframework.web.reactive.function.client.ClientResponse;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.Exceptions;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import reactor.util.retry.Retry;

@Service
public class RemoteCashoutApiImpl implements RemoteCashoutApi {

  private final WebClient webClient;
  private final int retryNumber;
  private final int retryTimeoutMillis;
  private final URI uri;
  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");
  private Message logMessage;

  public RemoteCashoutApiImpl(
      @Value("${openbet.cashout.url}") String baseUrl,
      @Value("${openbet.cashout.retry.number}") int retryNumber,
      @Value("${openbet.cashout.retry.timeout}") int retryTimeoutMillis,
      @Qualifier("cashoutWebClient") WebClient webClient)
      throws URISyntaxException {
    this.retryNumber = retryNumber;
    this.retryTimeoutMillis = retryTimeoutMillis;
    this.uri = new URI(baseUrl);
    this.webClient = webClient;
  }

  @SuppressWarnings("deprecation")
  @Override
  @Trace(dispatcher = true, metricName = "/oxi/cashoutV4")
  public Flux<CashoutOffer> getCashoutOffers(CashoutRequest request) {
    String requestJson = JsonUtil.toJson(request);
    logMessage = new Message();
    logMessage.setMessage(requestJson);
    ASYNC_LOGGER.debug("CashoutRequest:{}", logMessage);
    ExternalParameters params =
        HttpParameters.library("HttpClient")
            .uri(uri)
            .procedure("cashout calculation")
            .noInboundHeaders()
            .build();
    NewRelic.getAgent().getTracedMethod().reportAsExternal(params);
    final Token newRelicToken = NewRelic.getAgent().getTransaction().getToken();
    newRelicToken.expire();

    return webClient
        .method(HttpMethod.POST)
        .body(BodyInserters.fromValue(JsonUtil.toJson(request)))
        .accept(MediaType.APPLICATION_JSON)
        .exchange()
        .flatMap(response -> clientResponseToMono(request, response, newRelicToken))
        .flatMapMany(Flux::fromIterable)
        .retryWhen(Retry.fixedDelay(retryNumber, Duration.ofMillis(retryTimeoutMillis)));
  }

  @Trace(async = true)
  private Mono<List<CashoutOffer>> clientResponseToMono(
      CashoutRequest request, ClientResponse response, Token newRelicToken) {
    logMessage = new Message();
    newRelicToken.link();
    if (!response.statusCode().is2xxSuccessful()) {
      String message =
          MessageFormat.format(
              "Failed to connect to OB cashout service with request: {0}. Response status: {1}",
              JsonUtil.toJson(request), response.statusCode().value());
      NewRelic.noticeError(message);
      logMessage.setMessage(message);
      ASYNC_LOGGER.error(logMessage);
      return Mono.just(createErrorResponse());
    }
    return response
        .bodyToMono(CashoutOfferResponse.class)
        .map(
            cashoutOfferResponse -> {
              // if response contains message field that response is unsuccessful
              if (Objects.nonNull(cashoutOfferResponse.getMessage())) {
                String message =
                    MessageFormat.format(
                        "Failed response from OB cashout service with body: {0}. Reason: {1}",
                        JsonUtil.toJson(request), JsonUtil.toJson(cashoutOfferResponse));
                NewRelic.noticeError(message);
                return createErrorResponse();
              }
              return cashoutOfferResponse.getCashoutOffers();
            });
  }

  private List<CashoutOffer> createErrorResponse() {
    return Collections.singletonList(
        CashoutOffer.builder()
            .status(OPEN_BET_CASHOUT_SERVICE_FAILED_RESPONSE_ERROR.toString())
            .build());
  }

  private Function<Flux<Throwable>, Publisher<?>> onRetryAction(String path, Object requestObject) {
    int start = 1;
    return errorStream ->
        errorStream
            .zipWith(
                Flux.range(start, start + retryNumber),
                (error, index) -> {
                  if (error instanceof ReadTimeoutException) {
                    throw Exceptions.propagate(error);
                  }

                  if (index < start + retryNumber) {
                    return Pair.of(error, index);
                  } else {
                    throw Exceptions.propagate(error);
                  }
                })
            .flatMap(
                errorIndex -> {
                  Integer currentRetryNumber = errorIndex.getRight();
                  Throwable exception = errorIndex.getLeft();

                  trackRetries(currentRetryNumber, exception);

                  ASYNC_LOGGER.warn(
                      "Retried {} times from {}. Next retry in {} millis. Exception {}. Path: {}. Request body {}",
                      currentRetryNumber,
                      retryNumber,
                      currentRetryNumber < retryNumber ? retryTimeoutMillis : "[it was last retry]",
                      exception,
                      path,
                      JsonUtil.toJson(requestObject));
                  return Mono.delay(Duration.ofMillis(retryTimeoutMillis));
                });
  }

  private void trackRetries(Integer currentRetryNumber, Throwable exception) {
    NewRelic.incrementCounter(
        String.format(
            "Custom/Retry/CashoutApi/%s/%s",
            currentRetryNumber, exception.getClass().getSimpleName()));
  }
}

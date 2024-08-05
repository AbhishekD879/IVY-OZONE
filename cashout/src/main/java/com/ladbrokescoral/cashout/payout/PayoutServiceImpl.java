package com.ladbrokescoral.cashout.payout;

import com.fasterxml.jackson.databind.ObjectMapper;
import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.BodyInserters;
import org.springframework.web.reactive.function.client.ClientResponse;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;
import reactor.util.retry.Retry;

@Service
public class PayoutServiceImpl implements PayoutService {
  @Value("${payout.base.url}")
  String baseUrl;

  @Value("${payout.retry.number}")
  int retryNumber;

  @Value("${payout.retry.timeout}")
  int retryTimeoutMillis;

  private final WebClient webClient;

  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  @Autowired
  public PayoutServiceImpl(@Qualifier("payoutWebClient") WebClient webClient) {
    this.webClient = webClient;
  }

  private Mono<List<PotentialReturns>> getPotentialReturns(String request) {
    return this.webClient
        .method(HttpMethod.POST)
        .body(BodyInserters.fromValue(request))
        .accept(MediaType.APPLICATION_JSON)
        .exchangeToMono(
            (ClientResponse clientResponse) -> {
              if (clientResponse.statusCode().isError()) {
                return clientResponse.createException().flatMap(Mono::error);
              } else {
                return clientResponse.bodyToMono(
                    new ParameterizedTypeReference<List<PotentialReturns>>() {});
              }
            })
        .retryWhen(Retry.fixedDelay(retryNumber, Duration.ofMillis(retryTimeoutMillis)));
  }

  @Override
  public List<PotentialReturns> getPotentialReturns(List<PayoutRequest> payoutRequests) {
    List<PotentialReturns> potentialReturns = new ArrayList<>();
    try {
      ObjectMapper mapper = new ObjectMapper();
      String payoutRequestString = mapper.writeValueAsString(payoutRequests);
      ASYNC_LOGGER.debug("Payoutrequests:{}", payoutRequestString);
      potentialReturns = getPotentialReturns(payoutRequestString).toFuture().get();
      String potential = mapper.writeValueAsString(potentialReturns);
      ASYNC_LOGGER.debug("PotentialReturns:{}", potential);
    } catch (Exception e) {
      ASYNC_LOGGER.error("ERROR occuered while getting potentail returns: {}", e.getMessage());
    }
    return potentialReturns;
  }
}

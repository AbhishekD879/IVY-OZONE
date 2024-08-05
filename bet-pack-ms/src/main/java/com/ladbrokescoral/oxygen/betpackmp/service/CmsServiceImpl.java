package com.ladbrokescoral.oxygen.betpackmp.service;

import java.time.Duration;
import java.util.List;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;
import reactor.util.retry.Retry;

/*
 This class is processing cms calls
*/
@Service
@RequiredArgsConstructor
public class CmsServiceImpl implements CmsService {

  private final WebClient webClient;

  @Value("${cms.retry.number}")
  private int retryNumber;

  @Value("${cms.retry.timeout}")
  private int retryTimeoutMillis;

  @Override
  public Mono<List<String>> getActiveBetPackIds(String brand) {
    return this.webClient
        .method(HttpMethod.GET)
        .uri(builder -> builder.path("cms/api/{brand}/active-bet-pack-ids").build(brand))
        .accept(MediaType.APPLICATION_JSON)
        .retrieve()
        .bodyToMono(new ParameterizedTypeReference<List<String>>() {})
        .retryWhen(Retry.fixedDelay(this.retryNumber, Duration.ofMillis(this.retryTimeoutMillis)));
  }
}

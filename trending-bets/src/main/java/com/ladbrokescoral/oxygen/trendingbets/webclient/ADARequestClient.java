package com.ladbrokescoral.oxygen.trendingbets.webclient;

import com.ladbrokescoral.oxygen.trendingbets.dto.PersonalizedBets;
import com.ladbrokescoral.oxygen.trendingbets.model.ADARequestModel;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.ClientResponse;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

@Component
@RequiredArgsConstructor
@Slf4j
public class ADARequestClient {

  private static final String FANZONE = "Fanzone";

  private static final String FORYOU = "Foryou";

  @Qualifier("adaWebClient")
  private final WebClient webClient;

  @Value("${ada.baseUrl}")
  private String adaPersonalizedRecUrl;

  @Value("${ada.fzBaseUrl}")
  private String adaFanzoneRecUrl;

  @Value("${ada.apiKey}")
  private String adaApiKey;

  @Value("${ada.fzApiKey}")
  private String adaFzApiKey;

  public Mono<PersonalizedBets> executePersonalizedRequest(ADARequestModel body) {
    long startTime = System.currentTimeMillis();
    return webClient
        .method(HttpMethod.POST)
        .uri(
            getAdaUrl(body.isFanzoneWidgetRecs()),
            uriBuilder ->
                uriBuilder.queryParam("key", getApiKey(body.isFanzoneWidgetRecs())).build())
        .contentType(MediaType.APPLICATION_JSON)
        .bodyValue(body)
        .exchangeToMono(
            (ClientResponse response) -> {
              log.info(
                  "Time taken for {} ADA API {} :: {}",
                  body.isFanzoneWidgetRecs() ? FANZONE : FORYOU,
                  response.statusCode(),
                  System.currentTimeMillis() - startTime);
              if (response.statusCode().is2xxSuccessful()) {
                return response.bodyToMono(PersonalizedBets.class);
              } else {
                return response.createException().flatMap(Mono::error);
              }
            });
  }

  private String getAdaUrl(boolean isFzRequest) {
    return isFzRequest ? adaFanzoneRecUrl : adaPersonalizedRecUrl;
  }

  private String getApiKey(boolean isFzRequest) {
    return isFzRequest ? adaFzApiKey : adaApiKey;
  }
}

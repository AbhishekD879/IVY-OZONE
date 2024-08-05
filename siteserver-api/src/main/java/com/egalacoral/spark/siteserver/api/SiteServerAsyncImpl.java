package com.egalacoral.spark.siteserver.api;

import com.egalacoral.spark.siteserver.model.Children;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.SSResponse;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import java.util.stream.Collectors;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.http.client.reactive.ClientHttpConnector;
import org.springframework.web.reactive.function.client.ExchangeStrategies;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

public class SiteServerAsyncImpl implements SiteServerApiAsync {

  private WebClient webClient;
  private final String apiVersion;

  public SiteServerAsyncImpl(
      String baseUrl, String apiVersion, ClientHttpConnector connector, int maxMemorySize) {
    this.apiVersion = apiVersion;
    webClient =
        WebClient.builder()
            .baseUrl(baseUrl)
            .clientConnector(connector)
            .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .exchangeStrategies(
                ExchangeStrategies.builder()
                    .codecs(configurer -> configurer.defaultCodecs().maxInMemorySize(maxMemorySize))
                    .build())
            .build();
  }

  @Override
  public Mono<List<Event>> getEvents(SimpleFilter filter) {
    return getSSResponse(filter)
        .map(
            (SSResponse resp) ->
                resp.getChildren().stream()
                    .map(Children::getEvent)
                    .filter(Objects::nonNull)
                    .collect(Collectors.toList()));
  }

  private Mono<SSResponse> getSSResponse(SimpleFilter filter) {
    return webClient
        .method(HttpMethod.GET)
        .uri(
            uriBuilder ->
                uriBuilder
                    .path("openbet-ssviewer/Drilldown/{apiVersion}/Event")
                    .queryParam("simpleFilter", filter.getQueryMap())
                    .queryParam("translationLang", "en")
                    .queryParamIfPresent("existsFilter", Optional.empty())
                    .queryParam("includeUndisplayed", true)
                    .build(this.apiVersion))
        .accept(MediaType.APPLICATION_JSON)
        .retrieve()
        .bodyToMono(SSResponse.class);
  }
}

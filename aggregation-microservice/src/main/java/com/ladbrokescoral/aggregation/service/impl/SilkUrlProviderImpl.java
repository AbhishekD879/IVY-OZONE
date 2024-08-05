package com.ladbrokescoral.aggregation.service.impl;

import com.ladbrokescoral.aggregation.configuration.ApiProperties;
import com.ladbrokescoral.aggregation.exception.ErrorResponseProvider;
import com.ladbrokescoral.aggregation.model.Horse;
import com.ladbrokescoral.aggregation.model.RaceInfo;
import com.ladbrokescoral.aggregation.model.SilkUrl;
import com.ladbrokescoral.aggregation.service.SilkUrlProviderService;
import java.net.URI;
import java.nio.file.Paths;
import java.time.Duration;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.util.UriComponentsBuilder;
import reactor.core.publisher.Mono;

/** Class is responsible for fetching silks providers from df by event ids */
@Service
@Slf4j
public class SilkUrlProviderImpl implements SilkUrlProviderService {

  private final WebClient providerWebClientForSilks;
  private final String baseUrl;
  private final Duration timeout;

  @Autowired
  public SilkUrlProviderImpl(
      @Qualifier("providerWebClientForSilks") WebClient providerWebClientForSilks,
      ApiProperties properties) {
    this.providerWebClientForSilks = providerWebClientForSilks;
    this.baseUrl = properties.getDf().getEndpoint();
    this.timeout = properties.getDf().getTimeout();
  }

  @Override
  public Mono<List<SilkUrl>> getSilksUrlsByEventIds(String brand, List<String> eventIds) {
    URI uri =
        UriComponentsBuilder.fromHttpUrl(baseUrl)
            .pathSegment(brand, String.join(",", eventIds))
            .build()
            .toUri();
    return providerWebClientForSilks
        .get()
        .uri(uri)
        .retrieve()
        .bodyToMono(RaceInfo.class)
        .timeout(timeout)
        .doOnError(
            (Throwable error) ->
                log.error(
                    "error while calling the endpoint {} with message {}", uri, error.getMessage()))
        .flatMap(raceInfo -> Mono.just(createSilks(brand, raceInfo)));
  }

  private List<SilkUrl> createSilks(String brand, RaceInfo raceInfo) {
    if (raceInfo.isError()) {
      ErrorResponseProvider.handleSilkUrlProviderError(raceInfo.getErrorMessage());
    }
    List<SilkUrl> eventsSilkUrls = new ArrayList<>();
    raceInfo
        .getDocument()
        .values()
        .forEach(
            event -> {
              List<SilkUrl> silkUrls =
                  event.getHorses().stream()
                      .sorted(Comparator.comparing(Horse::getRpHorseId))
                      .map(
                          horse -> {
                            String endpoint =
                                "coral".equals(brand)
                                    ? horse.getSilkCoral()
                                    : horse.getSilkLadbrokes();
                            return SilkUrl.builder()
                                .endpoint(endpoint)
                                .silkId(extractId(endpoint))
                                .build();
                          })
                      .collect(Collectors.toList());
              eventsSilkUrls.addAll(silkUrls);
            });
    return eventsSilkUrls;
  }

  private String extractId(String endpoint) {

    String[] idWithExtension = Paths.get(endpoint).getFileName().toString().split("\\.");
    return idWithExtension.length > 0 ? idWithExtension[0] : "";
  }
}

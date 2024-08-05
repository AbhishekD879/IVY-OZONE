package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.configuration.ApiProperties;
import com.ladbrokescoral.oxygen.cms.configuration.ApiProperties.ApiConfiguration;
import com.newrelic.api.agent.NewRelic;
import java.time.Duration;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.Collections;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import java.util.stream.Collectors;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

@Component
@Slf4j
public class BanachService {

  private static final String LEAGUES_ENDPOINT = "api/v1/leagues";

  private final ApiProperties apiProperties;

  @Value("${banach.leagues.to-days-param:5}")
  private int toDaysParam;

  public BanachService(ApiProperties apiProperties) {
    this.apiProperties = apiProperties;
  }

  public List<Long> getBanachLeaguesIds(String brand) {

    ResponseEntity<GetLeaguesResponse> responseEntity = null;

    try {
      ApiConfiguration buildYourBetApiConfig = apiProperties.getBuildyourbet().get(brand);
      Objects.requireNonNull(
          buildYourBetApiConfig, "BuildYourBet config for brand=" + brand + " shouldn't be null");
      String requestUri =
          UriComponentsBuilder.fromHttpUrl(buildYourBetApiConfig.getUrl())
              .path(LEAGUES_ENDPOINT)
              .queryParam("fromEpochMillis", String.valueOf(Instant.now().toEpochMilli()))
              .queryParam("toEpochMillis", String.valueOf(calculateToEpochMillis()))
              .toUriString();
      log.debug("Executing byb request: '{}'", requestUri);
      responseEntity = new RestTemplate().getForEntity(requestUri, GetLeaguesResponse.class);

    } catch (Exception e) {
      log.error("Issue with retrieving leagues form build-bet-ms: {}", e.getMessage());
      NewRelic.noticeError(e);
    }

    List<GetLeaguesResponseDto> data =
        Optional.ofNullable(responseEntity)
            .map(ResponseEntity::getBody)
            .map(GetLeaguesResponse::getData)
            .orElse(Collections.emptyList());

    return data.stream()
        .filter(Objects::nonNull)
        .map(GetLeaguesResponseDto::getObTypeId)
        .collect(Collectors.toList());
  }

  private long calculateToEpochMillis() {
    return Instant.now()
        .truncatedTo(ChronoUnit.DAYS)
        .plus(Duration.ofDays(toDaysParam))
        .toEpochMilli();
  }

  @Data
  public static class GetLeaguesResponse {
    private List<GetLeaguesResponseDto> data;
  }

  @Data
  public static class GetLeaguesResponseDto {
    private Long obTypeId;
    private String title;
  }
}

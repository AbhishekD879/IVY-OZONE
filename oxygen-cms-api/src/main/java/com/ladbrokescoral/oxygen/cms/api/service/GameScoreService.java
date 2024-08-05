package com.ladbrokescoral.oxygen.cms.api.service;

import com.google.common.collect.ImmutableList;
import com.ladbrokescoral.oxygen.cms.api.entity.EventScore;
import com.ladbrokescoral.oxygen.cms.api.entity.EventScoreResponse;
import com.newrelic.api.agent.NewRelic;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClientResponseException;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

@Slf4j
@Service
public class GameScoreService {
  private static final String SCORE_PATH = "api/score";
  private static final String OTF_KEY_HEADER = "OTF-API-KEY";

  private final String otfUrl;
  private final HttpHeaders headers;

  private final RestTemplate restTemplate;

  public GameScoreService(
      @Value("${otf.url}") String otfUrl,
      @Value("${otf.key}") String otfKey,
      RestTemplate restTemplate) {
    this.otfUrl = otfUrl;
    this.headers = new HttpHeaders();
    this.headers.set(OTF_KEY_HEADER, otfKey);
    this.restTemplate = restTemplate;
  }

  public EventScoreResponse saveScore(String gameId, EventScore score) {
    try {
      sendSaveScoreRequest(gameId, score);
    } catch (RestClientResponseException e) {
      log.error("Issue with saving scores to OTF. ", e);
      NewRelic.noticeError(e);
      return new EventScoreResponse(e.getResponseBodyAsString(), false);
    } catch (Exception e) {
      log.error("Issue with saving scores to OTF. ", e);
      NewRelic.noticeError(e);
      return new EventScoreResponse(e.getMessage(), false);
    }
    return new EventScoreResponse(null, true);
  }

  public List<Integer> getScore(String eventId) {
    String requestUri =
        UriComponentsBuilder.fromHttpUrl(otfUrl)
            .path(SCORE_PATH)
            .pathSegment(eventId)
            .toUriString();
    HttpEntity<List<EventScore>> entity = new HttpEntity<>(headers);
    ResponseEntity<List<Integer>> responseEntity =
        restTemplate.exchange(
            requestUri, HttpMethod.GET, entity, new ParameterizedTypeReference<List<Integer>>() {});

    return responseEntity.getBody();
  }

  private void sendSaveScoreRequest(String gameId, EventScore eventScore) {
    String requestUri =
        UriComponentsBuilder.fromHttpUrl(otfUrl)
            .path(SCORE_PATH)
            .pathSegment(gameId)
            .queryParam("forceUpdate", true)
            .toUriString();
    log.debug("Executing otf score update request: '{}'", requestUri);
    HttpEntity<List<EventScore>> entity = new HttpEntity<>(ImmutableList.of(eventScore), headers);
    ResponseEntity<Void> exchange =
        restTemplate.exchange(requestUri, HttpMethod.PUT, entity, Void.class);
    log.debug("otf score update response status: {}", exchange.getStatusCodeValue());
  }
}

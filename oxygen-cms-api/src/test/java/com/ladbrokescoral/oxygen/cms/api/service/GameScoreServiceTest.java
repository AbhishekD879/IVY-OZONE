package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNull;
import static org.junit.Assert.assertTrue;
import static org.mockito.Matchers.eq;
import static org.mockito.Mockito.when;

import com.google.common.base.Charsets;
import com.ladbrokescoral.oxygen.cms.api.entity.EventScore;
import com.ladbrokescoral.oxygen.cms.api.entity.EventScoreResponse;
import java.util.Arrays;
import java.util.List;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Matchers;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestClientResponseException;
import org.springframework.web.client.RestTemplate;

@RunWith(MockitoJUnitRunner.class)
public class GameScoreServiceTest {

  @Mock private RestTemplate restTemplate;

  private String OTF_SCORE_PATH =
      "https://otf-stats-dev0.coralsports.dev.cloud.ladbrokescoral.com/";
  private String OTF_KEY = "key";

  private GameScoreService gameScoreService;

  @Before
  public void setUp() {
    gameScoreService = new GameScoreService(OTF_SCORE_PATH, OTF_KEY, restTemplate);
  }

  @Test
  public void saveScoreSuccessTest() {
    String gameID = "5cd03831c9e77c0001428484";
    EventScore eventScore = getEventScore();
    String scorePathForGame = getScorePathForGame(gameID);

    when(restTemplate.exchange(
            eq(scorePathForGame),
            eq(HttpMethod.PUT),
            Matchers.<HttpEntity<List<EventScore>>>any(),
            eq(Void.class)))
        .thenReturn(new ResponseEntity<>(HttpStatus.OK));

    EventScoreResponse response = gameScoreService.saveScore(gameID, eventScore);

    assertTrue(response.getIsSuccessfull());
    assertNull(response.getMessage());
  }

  @Test
  public void saveScoreFailureTest() {
    String gameID = "5cd03831c9e77c0001428484";
    EventScore eventScore = getEventScore();
    String scorePathForGame = getScorePathForGame(gameID);

    when(restTemplate.exchange(
            eq(scorePathForGame),
            eq(HttpMethod.PUT),
            Matchers.<HttpEntity<List<EventScore>>>any(),
            eq(Void.class)))
        .thenThrow(
            new RestClientResponseException(
                "error message",
                500,
                "INTERNAL_SERVER_ERROR",
                null,
                "error message".getBytes(),
                Charsets.UTF_8));

    EventScoreResponse response = gameScoreService.saveScore(gameID, eventScore);

    assertFalse(response.getIsSuccessfull());
    assertEquals("error message", response.getMessage());
  }

  @Test
  public void getScoreSuccessTest() {
    String eventId = "5cd03831c9e77c0001428484";
    String path = OTF_SCORE_PATH + "api/score/" + eventId;
    List<Integer> scores = Arrays.asList(3, 0);

    when(restTemplate.exchange(
            eq(path),
            eq(HttpMethod.GET),
            Matchers.<HttpEntity<List<EventScore>>>any(),
            eq(new ParameterizedTypeReference<List<Integer>>() {})))
        .thenReturn(new ResponseEntity<>(scores, HttpStatus.OK));

    assertEquals(gameScoreService.getScore(eventId), scores);
  }

  @Test(expected = RestClientException.class)
  public void getScoreFailureTest() {
    String eventId = "5cd03831c9e77c0001428484";
    String path = OTF_SCORE_PATH + "api/score/" + eventId;

    when(restTemplate.exchange(
            eq(path),
            eq(HttpMethod.GET),
            Matchers.<HttpEntity<List<EventScore>>>any(),
            eq(new ParameterizedTypeReference<List<Integer>>() {})))
        .thenThrow(new RestClientException("error message"));

    gameScoreService.getScore(eventId);
  }

  private EventScore getEventScore() {
    EventScore eventScore = new EventScore();
    eventScore.setEventId("eventId");
    eventScore.setEventPosition(0);
    eventScore.setActualScores(new Integer[] {1, 2});
    return eventScore;
  }

  private String getScorePathForGame(String gameID) {
    return OTF_SCORE_PATH + "api/score/" + gameID + "?forceUpdate=true";
  }
}

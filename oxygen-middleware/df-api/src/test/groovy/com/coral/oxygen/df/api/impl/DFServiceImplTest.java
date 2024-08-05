package com.coral.oxygen.df.api.impl;

import com.coral.oxygen.middleware.pojos.model.df.RaceEvent;
import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.Charset;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Map;
import java.util.Optional;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.mock.MockInterceptor;
import org.apache.commons.io.IOUtils;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class DFServiceImplTest {

  private static final int HORSE_RACE_CATEGORY_ID = 21;

  private static final int GREYHOUND_CATEGORY_ID = 19;

  private DFServiceImpl service;

  private MockInterceptor interceptor;

  @Before
  public void init() {
    interceptor = new MockInterceptor();

    OkHttpClient client = new OkHttpClient.Builder().addInterceptor(interceptor).build();

    service = new DFServiceImpl("http://test.com", "1", "11", client);
  }

  @Test
  public void getGreyhoundEvent() throws IOException {
    String body = body("df-grayhound.json");
    interceptor
        .addRule()
        .get(
            "http://test.com/1/sportsbook-api/categories/19/events/498694/content?locale=en-GB&api-key=11")
        .respond(body);

    Optional<RaceEvent> raceEvent = service.getRaceEvent(GREYHOUND_CATEGORY_ID, 498694L);
    Assert.assertTrue(raceEvent.isPresent());
    Assert.assertFalse(raceEvent.get().getRunners().isEmpty());
  }

  @Test
  public void getGreyhoundEvents() throws IOException {
    String body = body("df-grayhound.json");
    interceptor
        .addRule()
        .get(
            "http://test.com/1/sportsbook-api/categories/19/events/498694,13/content?locale=en-GB&api-key=11")
        .respond(body);

    Optional<Map<Long, RaceEvent>> raceEvent =
        service.getRaceEvents(GREYHOUND_CATEGORY_ID, Arrays.asList(498694L, 13L));
    Assert.assertTrue(raceEvent.isPresent());
    Assert.assertFalse(raceEvent.get().isEmpty());
  }

  @Test
  public void getHorseEvent() throws IOException {
    String body = body("df-horses.json");
    interceptor
        .addRule()
        .get(
            "http://test.com/1/sportsbook-api/categories/21/events/495481/content?locale=en-GB&api-key=11")
        .respond(body, MediaType.parse("application/json"));

    Optional<RaceEvent> raceEvent = service.getRaceEvent(HORSE_RACE_CATEGORY_ID, 495481L);
    Assert.assertTrue(raceEvent.isPresent());
    Assert.assertFalse(raceEvent.get().getHorses().isEmpty());
  }

  @Test
  public void getHorseEvents() throws IOException {
    String body = body("df-horses.json");
    interceptor
        .addRule()
        .get(
            "http://test.com/1/sportsbook-api/categories/21/events/495481,13/content?locale=en-GB&api-key=11")
        .respond(body, MediaType.parse("application/json"));

    Optional<Map<Long, RaceEvent>> raceEvent =
        service.getRaceEvents(HORSE_RACE_CATEGORY_ID, Arrays.asList(495481L, 13L));
    Assert.assertTrue(raceEvent.isPresent());
    Assert.assertFalse(raceEvent.get().isEmpty());
  }

  @Test
  public void getHorseEventsEmpty() throws IOException {
    String body = body("df-horses.json");
    interceptor
        .addRule()
        .get(
            "http://test.com/1/sportsbook-api/categories/21/events/495481,13/content?locale=en-GB&api-key=11")
        .respond(body, MediaType.parse("application/json"));

    Optional<Map<Long, RaceEvent>> raceEvent =
        service.getRaceEvents(HORSE_RACE_CATEGORY_ID, new ArrayList<>());
    Assert.assertFalse(raceEvent.isPresent());
  }

  @Test
  public void getHorseEventsMultiple() throws IOException {
    String body = body("df-horses-multiple.json");
    interceptor
        .addRule()
        .get(
            "http://test.com/1/sportsbook-api/categories/21/events/9890631,9890636,9890637,9890634,9890635,9890632,9890633/content?locale=en-GB&api-key=11")
        .respond(body, MediaType.parse("application/json"));

    Optional<Map<Long, RaceEvent>> raceEvent =
        service.getRaceEvents(
            HORSE_RACE_CATEGORY_ID,
            Arrays.asList(9890631L, 9890636L, 9890637L, 9890634L, 9890635L, 9890632L, 9890633L));
    Assert.assertTrue(raceEvent.isPresent());
    Assert.assertEquals(7, raceEvent.get().size());
  }

  @Test
  public void getHorseEventError() throws IOException {
    String body = body("df-horses-error.json");
    interceptor
        .addRule()
        .get(
            "http://test.com/1/sportsbook-api/categories/21/events/495481/content?locale=en-GB&api-key=11")
        .respond(body, MediaType.parse("application/json"));

    Optional<RaceEvent> raceEvent = service.getRaceEvent(HORSE_RACE_CATEGORY_ID, 495481L);
    Assert.assertFalse(raceEvent.isPresent());
  }

  private String body(String filename) throws IOException {
    InputStream resourceAsStream = getClass().getClassLoader().getResourceAsStream(filename);
    return IOUtils.toString(resourceAsStream, Charset.defaultCharset());
  }

  @Test
  public void getHorseEventEmptyMap() throws IOException {
    String body = body("df-horses-empty-map.json");
    interceptor
        .addRule()
        .get(
            "http://test.com/1/sportsbook-api/categories/21/events/495481/content?locale=en-GB&api-key=11")
        .respond(body, MediaType.parse("application/json"));

    Optional<RaceEvent> raceEvent = service.getRaceEvent(HORSE_RACE_CATEGORY_ID, 495481L);
    Assert.assertFalse(raceEvent.isPresent());
  }

  @Test
  public void get404ResponseCode() throws IOException {
    interceptor
        .addRule()
        .get(
            "http://test.com/1/sportsbook-api/categories/19/events/498694/content?locale=en-GB&api-key=11")
        .respond(404);

    Optional<RaceEvent> raceEvent = service.getRaceEvent(GREYHOUND_CATEGORY_ID, 498694L);
    Assert.assertFalse(raceEvent.isPresent());
  }

  @Test
  public void get404HorseEventsMultiple() throws IOException {
    interceptor
        .addRule()
        .get(
            "http://test.com/1/sportsbook-api/categories/21/events/9890631,9890636,9890637,9890634,9890635,9890632,9890633/content?locale=en-GB&api-key=11")
        .respond(404);

    Optional<Map<Long, RaceEvent>> raceEvent =
        service.getRaceEvents(
            HORSE_RACE_CATEGORY_ID,
            Arrays.asList(9890631L, 9890636L, 9890637L, 9890634L, 9890635L, 9890632L, 9890633L));
    Assert.assertFalse(raceEvent.isPresent());
  }

  @Test
  public void get503HorseEventsMultiple() throws IOException {
    interceptor
        .addRule()
        .get(
            "http://test.com/1/sportsbook-api/categories/21/events/9890631,9890636,9890637,9890634,9890635,9890632,9890633/content?locale=en-GB&api-key=11")
        .respond(503);

    Optional<Map<Long, RaceEvent>> raceEvent =
        service.getRaceEvents(
            HORSE_RACE_CATEGORY_ID,
            Arrays.asList(9890631L, 9890636L, 9890637L, 9890634L, 9890635L, 9890632L, 9890633L));
    Assert.assertFalse(raceEvent.isPresent());
  }
}

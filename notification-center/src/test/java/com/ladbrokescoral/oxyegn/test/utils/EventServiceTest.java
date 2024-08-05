package com.ladbrokescoral.oxyegn.test.utils;

import static com.ladbrokescoral.oxyegn.test.utils.Utils.fromFile;
import static org.junit.Assert.*;
import static org.mockito.Matchers.startsWith;
import static org.mockito.Mockito.doReturn;

import com.egalacoral.spark.siteserver.model.Event;
import com.google.gson.Gson;
import com.google.gson.JsonParser;
import com.ladbrokescoral.oxygen.notification.services.ConsumeEventException;
import com.ladbrokescoral.oxygen.notification.services.EventService;
import com.ladbrokescoral.oxygen.notification.services.SiteServerApiService;
import com.ladbrokescoral.oxygen.notification.services.repositories.Events;
import com.ladbrokescoral.oxygen.notification.utils.RedisKey;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import org.apache.commons.io.IOUtils;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Rule;
import org.junit.Test;
import org.junit.rules.ExpectedException;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class EventServiceTest {

  @Mock private SiteServerApiService siteServerApiService;
  @Mock private Events events;
  private Gson gson = new Gson();

  private EventService eventService;
  private List<String> testEventIds =
      Arrays.asList("6223898", "11010680", "11011284", "11017974", "11021181", "123", "1234");

  @Rule public ExpectedException thrown = ExpectedException.none();

  @Before
  public void setUp() {
    eventService = new EventService(siteServerApiService, events);

    testEventIds.forEach(
        eventId ->
            doReturn(Optional.of(fromFile(gson, "ssEvents/" + eventId + ".json", Event.class)))
                .when(siteServerApiService)
                .getEvent(eventId));
  }

  @Test
  public void processTest() throws IOException {
    for (String eventId : testEventIds) {
      String expected = getResourceAsString("events/" + eventId + ".json");
      Assert.assertTrue(
          assertEqualsEventFields(expected, eventService.process(Long.parseLong(eventId))));
    }
  }

  private String getResourceAsString(String name) throws IOException {
    return IOUtils.toString(
        EventServiceTest.class.getClassLoader().getResourceAsStream(name), StandardCharsets.UTF_8);
  }

  @Test
  public void getProcessedEventTest() {
    assertFalse(eventService.getProcessedEvent(6223898).isPresent());
    doReturn(Optional.of(new Event())).when(events).findById(RedisKey.forEvent(6223898L));
    assertTrue(eventService.getProcessedEvent(6223898).isPresent());
  }

  @Test
  public void failedToConsumeEventTest() {
    doReturn(Optional.empty()).when(siteServerApiService).getEvent("111");
    thrown.expect(ConsumeEventException.class);
    thrown.expectMessage("Can't load initial data for event id: 111");
    eventService.process(111);

    doReturn(Optional.of(new Event())).when(siteServerApiService).getEvent("222");
    thrown.expect(ConsumeEventException.class);
    thrown.expectMessage(startsWith("Can't parse initial data for event: "));
    eventService.process(222);
  }

  private boolean assertEqualsEventFields(
      String expectedEvent,
      com.ladbrokescoral.oxygen.notification.entities.sportsbook.Event actual) {
    String actualAsString = gson.toJson(actual);
    assertEquals(
        String.format("Expected '%s', got '%s'", expectedEvent, actualAsString),
        new JsonParser().parse(expectedEvent),
        new JsonParser().parse(actualAsString));
    return true;
  }
}

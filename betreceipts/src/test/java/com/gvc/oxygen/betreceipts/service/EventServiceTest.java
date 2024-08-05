package com.gvc.oxygen.betreceipts.service;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.gvc.oxygen.betreceipts.dto.MetaEvent;
import com.gvc.oxygen.betreceipts.entity.NextRace;
import com.gvc.oxygen.betreceipts.entity.NextRaceMap;
import com.gvc.oxygen.betreceipts.exceptions.JsonSerializeDeserializeException;
import com.gvc.oxygen.betreceipts.repository.EventRepository;
import com.gvc.oxygen.betreceipts.repository.MetaEventRepository;
import java.time.Instant;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import org.assertj.core.api.WithAssertions;
import org.junit.Assert;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class EventServiceTest implements WithAssertions {

  @Mock private EventRepository eventRepository;

  @Mock private MetaEventRepository metaEventRepository;

  @Mock ObjectMapper objectMapperMock;

  @InjectMocks private EventService eventService;

  @Test
  void testSaveMetaEvents() {
    Assertions.assertDoesNotThrow(() -> eventService.saveMetaEvents(getMetaEvents()));
  }

  @Test
  void testDeleteAllMetaEvents() {
    Assertions.assertDoesNotThrow(() -> eventService.deleteAllMetaEvents());
  }

  @Test
  void testDeleteNextRaceMap() {
    Assertions.assertDoesNotThrow(() -> eventService.deleteNextRaceMap("1"));
  }

  @Test
  void testDeleteMetaEvent() {
    Assertions.assertDoesNotThrow(() -> eventService.deleteMetaEvent("1"));
  }

  @Test
  void testSaveNextRaceMap() {
    Assertions.assertDoesNotThrow(() -> eventService.saveNextRaceMap(createNextRaceMap()));
  }

  @Test
  void testSaveAllNextRaceMap() {
    Assertions.assertDoesNotThrow(
        () -> eventService.saveNextRaceMap(Arrays.asList(createNextRaceMap())));
  }

  @Test
  void testNextRaceMapById() {
    Mockito.when(eventRepository.findById("1")).thenReturn(Optional.of(createNextRaceMap()));
    Assertions.assertDoesNotThrow(() -> eventService.getNextRaceMapById("1"));
  }

  @Test
  void testEventMapToEven() throws JsonProcessingException {
    EventService eventService1 =
        new EventService(eventRepository, metaEventRepository, objectMapperMock);
    Mockito.doThrow(new JsonProcessingException("error in processing") {})
        .when(objectMapperMock)
        .readValue(Mockito.anyString(), Mockito.eq(NextRace.class));
    try {
      eventService1.eventMapToEven(createNextRaceMap());
    } catch (JsonSerializeDeserializeException ex) {
      Assert.assertEquals("Error in Deserialization from NextRace", ex.getMessage());
    }
  }

  private List<MetaEvent> getMetaEvents() {
    return Arrays.asList(createMetaEvent());
  }

  private MetaEvent createMetaEvent() {
    MetaEvent metaEvent = new MetaEvent();
    metaEvent.setEventId("123");
    metaEvent.setStartTime(Instant.now());
    metaEvent.setTipAvailable(true);
    return metaEvent;
  }

  private NextRaceMap createNextRaceMap() {
    return new NextRaceMap("2", "{}", 3);
  }
}

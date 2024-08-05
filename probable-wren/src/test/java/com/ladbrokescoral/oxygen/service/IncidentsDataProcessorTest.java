package com.ladbrokescoral.oxygen.service;

import static org.mockito.Mockito.*;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.dto.messages.IncidentMessage;
import java.util.*;
import java.util.concurrent.CompletableFuture;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.test.util.ReflectionTestUtils;

@ExtendWith(MockitoExtension.class)
class IncidentsDataProcessorTest {

  private static final String CHANNEL = "222211218";
  IncidentsDataProcessor incidentsDataProcessor;
  @Mock RedisOperations redisOperations;
  private List<Integer> cacheCodes = Arrays.asList(2, 6);
  String MESSAGE =
      "{\"incident\":{\"eventId\":\"fake593f-d146-4092-ad46-8bdf192b6ebb\",\"correlationId\":\"7645316d-ddc8-42c9-ac4e-e6668704a5f6\",\"seqId\":null,\"type\":{\"code\":601,\"description\":\"VAR\"},\"score\":null,\"periodScore\":null,\"clock\":\"46:32\",\"participant\":\"AWAY\",\"period\":\"1h\",\"timeStamp\":\"2022-01-03T12:43:40.342Z\",\"receiveTimestamp\":\"2020-07-15T23:37:07.478Z\",\"context\":{\"teamName\":\"Liverpool\",\"playerName\":\"G. Wijnaldum\",\"reasonId\":601,\"x\":\"0\",\"y\":\"0\"},\"feed\":\"OPTA\"}}";
  private static final String EVENTID = "222211218";
  private int ttl = 600;

  @BeforeEach
  public void init() {
    incidentsDataProcessor = new IncidentsDataProcessor(redisOperations, new ObjectMapper());
  }

  @Test
  void incidentsDataCacheTest() throws JsonProcessingException {
    ConsumerRecord<String, String> record =
        new ConsumerRecord<String, String>("topic", 0, 0, EVENTID, MESSAGE);
    Map<String, Object> incidentResponse =
        new ObjectMapper().readValue(record.value(), new TypeReference<Map<String, Object>>() {});
    ((Map<String, Object>) incidentResponse.get("incident")).put("eventId", record.key());
    when(redisOperations.getIncidentLastMessage(CHANNEL))
        .thenReturn(
            CompletableFuture.completedFuture(
                Optional.of(new IncidentMessage(CHANNEL, MESSAGE, ttl))));
    ReflectionTestUtils.setField(incidentsDataProcessor, "cacheCodes", cacheCodes);
    incidentsDataProcessor.incidentsDataIntoCache(record, incidentResponse);
    verify(redisOperations, times(1)).getIncidentLastMessage(any());
  }

  @Test
  void incidentsDataEmptyCacheCodesTest() throws JsonProcessingException {
    ConsumerRecord<String, String> record =
        new ConsumerRecord<String, String>("topic", 0, 0, EVENTID, MESSAGE);
    Map<String, Object> incidentResponse =
        new ObjectMapper().readValue(record.value(), new TypeReference<Map<String, Object>>() {});
    ((Map<String, Object>) incidentResponse.get("incident")).put("eventId", record.key());

    when(redisOperations.getIncidentLastMessage(CHANNEL))
        .thenReturn(
            CompletableFuture.completedFuture(
                Optional.of(new IncidentMessage(CHANNEL, MESSAGE, ttl))));
    redisOperations.saveLastIncidentMessage(new IncidentMessage(CHANNEL, MESSAGE, ttl));
    ReflectionTestUtils.setField(incidentsDataProcessor, "cacheCodes", null);
    incidentsDataProcessor.incidentsDataIntoCache(record, incidentResponse);
    verify(redisOperations, times(1)).getIncidentLastMessage(any());
  }

  @Test
  void incidentsDataEmptyGetCacheCodesTest() throws JsonProcessingException {
    ConsumerRecord<String, String> record =
        new ConsumerRecord<String, String>("topic", 0, 0, "12345", MESSAGE);
    Map<String, Object> incidentResponse =
        new ObjectMapper().readValue(record.value(), new TypeReference<Map<String, Object>>() {});
    ((Map<String, Object>) incidentResponse.get("incident")).put("eventId", record.key());
    when(redisOperations.getIncidentLastMessage("12345"))
        .thenReturn(CompletableFuture.completedFuture(Optional.empty()));
    redisOperations.saveLastIncidentMessage(new IncidentMessage("123456", MESSAGE, ttl));
    ReflectionTestUtils.setField(incidentsDataProcessor, "cacheCodes", null);
    incidentsDataProcessor.incidentsDataIntoCache(record, incidentResponse);
    verify(redisOperations, times(1)).getIncidentLastMessage(any());
  }

  @Test
  void incidentsDataCacheCodeTest() throws JsonProcessingException {
    String MESSAGE =
        "{\"incident\":{\"eventId\":\"fake593f-d146-4092-ad46-8bdf192b6ebb\",\"correlationId\":\"7645316d-ddc8-42c9-ac4e-e6668704a5f6\",\"seqId\":null,\"type\":{\"code\":6,\"description\":\"VAR\"},\"score\":null,\"periodScore\":null,\"clock\":\"46:32\",\"participant\":\"AWAY\",\"period\":\"1h\",\"timeStamp\":\"2022-01-03T12:43:40.342Z\",\"receiveTimestamp\":\"2020-07-15T23:37:07.478Z\",\"context\":{\"teamName\":\"Liverpool\",\"playerName\":\"G. Wijnaldum\",\"reasonId\":601,\"x\":\"0\",\"y\":\"0\"},\"feed\":\"OPTA\"}}";
    ConsumerRecord<String, String> record =
        new ConsumerRecord<String, String>("topic", 0, 0, EVENTID, MESSAGE);
    Map<String, Object> incidentResponse =
        new ObjectMapper().readValue(record.value(), new TypeReference<Map<String, Object>>() {});
    ((Map<String, Object>) incidentResponse.get("incident")).put("eventId", record.key());
    ReflectionTestUtils.setField(incidentsDataProcessor, "cacheCodes", cacheCodes);
    incidentsDataProcessor.incidentsDataIntoCache(record, incidentResponse);
    verify(redisOperations, times(1)).saveLastIncidentMessage(any());
  }

  @Test
  void incidentsDataCacheCodeExceptionTest() {
    String MESSAGE = "";
    ConsumerRecord<String, String> record =
        new ConsumerRecord<String, String>("topic", 0, 0, EVENTID, MESSAGE);
    Map<String, Object> incidentResponse = new HashMap<>();
    incidentsDataProcessor.incidentsDataIntoCache(record, incidentResponse);
    verify(redisOperations, times(0)).saveLastIncidentMessage(any());
  }
}

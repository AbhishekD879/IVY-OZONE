package com.ladbrokescoral.oxygen.service;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.dto.messages.IncidentDto;
import com.ladbrokescoral.oxygen.dto.messages.IncidentMessage;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Slf4j
@Component
@RequiredArgsConstructor
public class IncidentsDataProcessor {

  private final RedisOperations redisOperations;
  private final ObjectMapper objectMapper;

  @Value("${incident.cache.codes}")
  private List<Integer> cacheCodes;

  @Value("${incident.ttl}")
  private long ttl;

  public void incidentsDataIntoCache(
      ConsumerRecord<String, String> incidentsData, Map<String, Object> incidentResponse) {

    try {
      IncidentDto incidentsDto = objectMapper.readValue(incidentsData.value(), IncidentDto.class);

      if (cacheCodes != null
          && cacheCodes.stream()
              .anyMatch(code -> code.equals(incidentsDto.getIncident().getType().getCode()))) {
        redisOperations.saveLastIncidentMessage(
            new IncidentMessage(
                incidentsData.key(), new ObjectMapper().writeValueAsString(incidentResponse), ttl));
      } else {
        redisOperations
            .getIncidentLastMessage(incidentsData.key())
            .thenAccept(
                (Optional<IncidentMessage> optionalIncident) -> {
                  if (optionalIncident.isPresent()) {
                    log.info("clearing from Cache in kafkaListener {} ", optionalIncident.get());
                    redisOperations.clearIncidentMessage(optionalIncident.get());
                  }
                });
      }
    } catch (JsonProcessingException e) {
      log.error("Can not parse IncidentsDataProcessor update {}", e.getMessage());
    }
  }
}

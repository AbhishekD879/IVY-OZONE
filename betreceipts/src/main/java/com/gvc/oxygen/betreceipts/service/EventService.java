package com.gvc.oxygen.betreceipts.service;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.common.cache.Cache;
import com.google.common.cache.CacheBuilder;
import com.gvc.oxygen.betreceipts.dto.MetaEvent;
import com.gvc.oxygen.betreceipts.entity.NextRace;
import com.gvc.oxygen.betreceipts.entity.NextRaceMap;
import com.gvc.oxygen.betreceipts.exceptions.JsonSerializeDeserializeException;
import com.gvc.oxygen.betreceipts.repository.EventRepository;
import com.gvc.oxygen.betreceipts.repository.MetaEventRepository;
import java.time.Duration;
import java.time.Instant;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;
import java.util.stream.StreamSupport;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;
import reactor.core.publisher.Flux;

@Service
@RequiredArgsConstructor
@Slf4j
public class EventService {

  public static final Comparator<MetaEvent> START_TIME_COMPARATOR =
      Comparator.comparing(
          MetaEvent::getStartTime, Comparator.nullsLast(Comparator.naturalOrder()));

  private final EventRepository eventRepository;

  private final MetaEventRepository metaEventRepository;

  private final ObjectMapper objectMapper;

  public static final int EXPIRE_IN = 15;
  private static Cache<String, List<MetaEvent>> cache =
      CacheBuilder.newBuilder().expireAfterWrite(EXPIRE_IN, TimeUnit.MINUTES).build();

  public Flux<MetaEvent> getMetaEvents() {
    List<MetaEvent> metaEvents =
        CollectionUtils.isEmpty(getCache()) ? setCache(metaEventRepository.findAll()) : getCache();
    log.info("Events from cache {}", metaEvents.size());
    return Flux.fromIterable(metaEvents)
        .filter(meta -> Instant.now().isBefore(meta.getStartTime()))
        .sort(START_TIME_COMPARATOR);
  }

  public Iterable<MetaEvent> saveMetaEvents(List<MetaEvent> metaEvents) {
    return metaEventRepository.saveAll(metaEvents);
  }

  public void deleteAllMetaEvents() {
    metaEventRepository.deleteAll();
  }

  public void deleteNextRaceMap(String id) {
    eventRepository.deleteById(id);
  }

  public void deleteMetaEvent(String id) {
    metaEventRepository.deleteById(id);
  }

  public Iterable<NextRaceMap> saveNextRaceMap(List<NextRaceMap> events) {
    return eventRepository.saveAll(events);
  }

  public NextRaceMap saveNextRaceMap(NextRaceMap nextRaceMap) {
    return eventRepository.save(nextRaceMap);
  }

  public Optional<NextRaceMap> getNextRaceMapById(String eventId) {
    return eventRepository.findById(eventId);
  }

  public List<NextRace> getEventsByIds(List<String> ids) {
    Instant start = Instant.now();
    Iterable<NextRaceMap> eventMaps = eventRepository.findAllById(ids);
    log.info(
        "time taken to fetch all next races {}", Duration.between(start, Instant.now()).toMillis());
    return StreamSupport.stream(eventMaps.spliterator(), false)
        .map(this::eventMapToEven)
        .collect(Collectors.toCollection(ArrayList::new));
  }

  public NextRace eventMapToEven(NextRaceMap nextRaceMap) {
    NextRace nextRace = null;
    try {
      nextRace = objectMapper.readValue(nextRaceMap.getNextRace(), NextRace.class);
    } catch (JsonProcessingException exception) {
      throw new JsonSerializeDeserializeException(
          "Error in Deserialization from NextRace", exception.getCause());
    }
    return nextRace;
  }

  public List<MetaEvent> setCache(List<MetaEvent> events) {
    cache.put("1", events);
    return events;
  }

  public List<MetaEvent> getCache() {
    return cache.getIfPresent("1");
  }
}

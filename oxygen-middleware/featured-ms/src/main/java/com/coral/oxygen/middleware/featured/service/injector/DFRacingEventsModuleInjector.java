package com.coral.oxygen.middleware.featured.service.injector;

import com.coral.oxygen.df.api.DFService;
import com.coral.oxygen.middleware.common.mappers.DFGreyhoundRacingOutcomeMapper;
import com.coral.oxygen.middleware.common.mappers.DFHorseRacingOutcomeMapper;
import com.coral.oxygen.middleware.common.mappers.DFRaceOutcomeMapper;
import com.coral.oxygen.middleware.common.mappers.DFRacingEventDataMapper;
import com.coral.oxygen.middleware.common.service.ModuleAdapter;
import com.coral.oxygen.middleware.common.service.featured.IdsCollector;
import com.coral.oxygen.middleware.pojos.model.df.RaceEvent;
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.coral.oxygen.middleware.pojos.model.output.OutputMarket;
import com.coral.oxygen.middleware.pojos.model.output.OutputOutcome;
import java.util.Collection;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.stream.Collectors;
import lombok.EqualsAndHashCode;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.util.ObjectUtils;

@Component
@Slf4j
public class DFRacingEventsModuleInjector extends ModuleAdapter implements EventsModuleInjector {

  private final DFService dfService;
  private DFRacingEventDataMapper dfRacingEventDataMapper;

  private Map<Integer, DFRaceOutcomeMapper> mapperMap = new HashMap<>();

  @Autowired
  public DFRacingEventsModuleInjector(
      DFService dfService,
      DFHorseRacingOutcomeMapper horseRacingOutcomeMapper,
      DFGreyhoundRacingOutcomeMapper grayHoundRacingOutcomeMapper,
      DFRacingEventDataMapper dfRacingEventDataMapper) {
    this.dfService = dfService;
    this.dfRacingEventDataMapper = dfRacingEventDataMapper;
    registerMapper(horseRacingOutcomeMapper);
    registerMapper(grayHoundRacingOutcomeMapper);
  }

  private void registerMapper(DFRaceOutcomeMapper horseRacingOutcomeMapper) {
    this.mapperMap.put(horseRacingOutcomeMapper.getCategoryId(), horseRacingOutcomeMapper);
  }

  public void injectData(List<? extends EventsModuleData> items, IdsCollector idsCollector) {
    Collection<Long> racingEventsIds = new HashSet<>(idsCollector.getRacingEventsIds());
    Collection<Long> selectedByMarketEventIds = getSelectedByMarketRacingEventsIds(items);
    racingEventsIds.addAll(selectedByMarketEventIds);

    Map<RaceKey, RaceEvent> racingEventsMap = consumeRacingEvents(racingEventsIds);

    items.stream()
        .filter(d -> d.getId() != null)
        .filter(d -> !ObjectUtils.isEmpty(d.getCategoryId()))
        .filter(d -> d.getOutcomeId() == null) // only whole events should be processed here
        .filter(
            d -> racingEventsMap.containsKey(createKey(d))) // only whole events should be processed
        // here
        .forEach(d -> mapEvent(racingEventsMap, d));
  }

  private void mapEvent(Map<RaceKey, RaceEvent> racingEventsMap, EventsModuleData d) {
    Integer categoryId = Integer.valueOf(d.getCategoryId());
    RaceKey raceKey = new RaceKey(categoryId, d.getId());
    RaceEvent raceEvent = racingEventsMap.get(raceKey);
    if (!ObjectUtils.isEmpty(raceEvent)) {
      dfRacingEventDataMapper.map(d, raceEvent);
      mapOutcomes(d, raceEvent);
    }
  }

  private void mapOutcomes(EventsModuleData d, RaceEvent raceEvent) {
    d.getMarkets().stream()
        .filter(Objects::nonNull)
        .map(OutputMarket::getOutcomes)
        .filter(Objects::nonNull)
        .flatMap(Collection::stream)
        .forEach(o -> mapRacingOutcome(o, d, raceEvent));
  }

  private RaceKey createKey(EventsModuleData d) {
    return new RaceKey(Integer.valueOf(d.getCategoryId()), d.getId());
  }

  private void mapRacingOutcome(OutputOutcome outcome, EventsModuleData data, RaceEvent raceEvent) {
    Integer categoryId = Integer.valueOf(data.getCategoryId());
    if (!ObjectUtils.isEmpty(outcome.getRunnerNumber())) {
      DFRaceOutcomeMapper outcomeMapper = mapperMap.get(categoryId);
      if (!ObjectUtils.isEmpty(outcomeMapper)) {
        outcomeMapper.map(outcome, raceEvent);
      } else {
        log.info("Ignore data with unknown categoryId {}", data.getCategoryId());
      }
    } else {
      log.info("Can't map race info by id {}", data.getId());
    }
  }

  private Collection<Long> getSelectedByMarketRacingEventsIds(
      List<? extends EventsModuleData> items) {
    return items.stream()
        .filter(e -> e.getMarketId() != null && isRacingEvent(e))
        .map(EventsModuleData::getId)
        .collect(Collectors.toSet());
  }

  private boolean isRacingEvent(EventsModuleData e) {
    return mapperMap.keySet().stream()
            .filter(id -> String.valueOf(id).equals(e.getCategoryId()))
            .count()
        > 0;
  }

  private Map<RaceKey, RaceEvent> consumeRacingEvents(Collection<Long> eventsIds) {
    Map<RaceKey, RaceEvent> eventMap = new HashMap<>();
    mapperMap.keySet().stream()
        .forEach(
            categoryId -> {
              Optional<Map<Long, RaceEvent>> events =
                  dfService.getRaceEvents(categoryId, eventsIds);
              if (events.isPresent()) {
                Map<Long, RaceEvent> map = events.get();
                map.forEach(
                    (id, event) -> {
                      RaceKey raceKey = new RaceKey(categoryId, id);
                      eventMap.put(raceKey, event);
                    });
              }
            });
    return eventMap;
  }

  @RequiredArgsConstructor
  @EqualsAndHashCode
  private class RaceKey {

    private final Integer categoryId;
    private final Long eventId;
  }
}

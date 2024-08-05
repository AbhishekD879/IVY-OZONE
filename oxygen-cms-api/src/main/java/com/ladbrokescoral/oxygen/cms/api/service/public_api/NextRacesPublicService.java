package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.coral.oxygen.df.model.RaceEvent;
import com.egalacoral.spark.siteserver.model.Event;
import com.ladbrokescoral.oxygen.cms.api.entity.NextRace;
import com.ladbrokescoral.oxygen.cms.api.entity.NextRacesResult;
import com.ladbrokescoral.oxygen.cms.api.entity.TypeFlagCodes;
import com.ladbrokescoral.oxygen.cms.api.mapping.NextRaceMapper;
import com.ladbrokescoral.oxygen.cms.api.service.df.DFService;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.NextEventsParameters;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.NextEventsParameters.NextEventsParametersBuilder;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeService;
import java.io.IOException;
import java.time.Duration;
import java.time.LocalTime;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;

@Slf4j
@Service
public class NextRacesPublicService {

  public static final Comparator<Event> START_TIME_COMPARATOR =
      Comparator.comparing(Event::getStartTime, Comparator.nullsLast(Comparator.naturalOrder()));

  public static final String UK = "UK";
  public static final String IRE = "IRE";
  public static final String INT = "INT";

  private SiteServeService siteServerService;

  private DFService dfService;

  @Value("${nextRaces.timePeriodMinutes:15}")
  private int timePeriodMinutes;

  @Value("${nextRaces.numberOfNextRaces:3}")
  private int maxNextRaces;

  @Value("${nextRaces.categoryId:21}")
  private int categoryId;

  @Autowired
  public NextRacesPublicService(SiteServeService siteServerService, DFService dfService) {
    this.siteServerService = siteServerService;
    this.dfService = dfService;
  }

  /**
   * Find next races in next 15 min. If we hae any UK&IR races in next 15. min. group them and
   * return. If we don't UK&IR races and have any international group them and return. * If We don't
   * have any races in next 15. min. Fetch today races and Return. * If we don't have any races
   * today. Fetch tomorrow races and return ad per maxNextRaces limit.
   *
   * @param brand
   * @return Returns NextRacesResult list.
   * @throws IOException
   */
  public NextRacesResult find(String brand) throws IOException {
    final List<Event> nextEvents = new ArrayList<>();
    NextRacesResult result = new NextRacesResult();
    result.setUkAndIre(true);

    nextEvents.addAll(getNextEvents(brand, result));

    if (nextEvents.isEmpty()) {
      // get today or tomorrow races.
      nextEvents.addAll(getTodayOrTomorrowEvents(brand));
    }

    if (!nextEvents.isEmpty()) {
      List<NextRace> nextRaces = new ArrayList<>();
      List<Long> eventIds = getEventIds(nextEvents);
      Optional<Map<Long, RaceEvent>> races = dfService.getNextRaces(brand, categoryId, eventIds);
      races.ifPresent(r -> nextRaces.addAll(merge(r, nextEvents)));

      if (nextRaces.isEmpty()) {
        nextRaces.addAll(
            nextEvents.stream().map(NextRaceMapper.INSTANCE::toDto).collect(Collectors.toList()));
      }
      result.setRaces(nextRaces);
    }

    return result;
  }

  /** Method that returns next 15 min. events */
  private List<? extends Event> getNextEvents(String brand, NextRacesResult result) {

    List<? extends Event> nextEvents = null;
    List<Event> allEvents = getSiteServerEvents(brand, timePeriodMinutes);

    if (!CollectionUtils.isEmpty(allEvents)) {
      // Group the next events if we have UK or IRE give priority to them.
      nextEvents = filterNextEvents(allEvents, TypeFlagCodes.of(UK, IRE));

      if (CollectionUtils.isEmpty(nextEvents)) {
        nextEvents = filterNextEvents(allEvents, TypeFlagCodes.of(INT));
        result.setUkAndIre(false);
      }
      log.debug("Got next 15 min. events with size {}", nextEvents.size());
    }

    return CollectionUtils.isEmpty(nextEvents) ? Collections.emptyList() : nextEvents;
  }

  /** Method for getting today or tomorrow events */
  private List<? extends Event> getTodayOrTomorrowEvents(String brand) {

    int remainingMinutes =
        (int) Duration.between(LocalTime.now(), LocalTime.MAX).plusDays(1).toMinutes();

    // get events util tomorrow.
    List<Event> allEvents = getSiteServerEvents(brand, remainingMinutes);

    if (!CollectionUtils.isEmpty(allEvents)) {
      allEvents = allEvents.stream().limit(maxNextRaces).collect(Collectors.toList());
    }
    return allEvents;
  }

  private List<Event> filterNextEvents(List<Event> allEvents, TypeFlagCodes of) {
    return allEvents.stream()
        .filter(e -> TypeFlagCodes.of(e.getTypeFlagCodes()).contains(of))
        .limit(maxNextRaces)
        .collect(Collectors.toList());
  }

  private List<Long> getEventIds(List<Event> events) {
    return events.stream().map(Event::getId).map(Long::valueOf).collect(Collectors.toList());
  }

  private List<Event> getSiteServerEvents(String brand, int timePeriodMinutes) {
    NextEventsParametersBuilder paramsBuilder = NextEventsParameters.builder();
    paramsBuilder
        .brand(brand)
        .typeFlagCodes(TypeFlagCodes.of(UK, IRE, INT))
        .timePeriodMinutes(timePeriodMinutes)
        .categoryId(categoryId)
        .comparator(START_TIME_COMPARATOR);
    return siteServerService.getNextEvents(paramsBuilder.build());
  }

  private List<NextRace> merge(Map<Long, RaceEvent> document, List<Event> events) {
    return events.stream().map(e -> buildNextRace(document, e)).collect(Collectors.toList());
  }

  private NextRace buildNextRace(Map<Long, RaceEvent> document, Event e) {
    NextRace nextRace;
    Optional<RaceEvent> raceEvent = Optional.ofNullable(document.get(Long.valueOf(e.getId())));

    if (raceEvent.isPresent()) {
      nextRace = NextRaceMapper.INSTANCE.toDto(e, raceEvent.get());
    } else {
      nextRace = NextRaceMapper.INSTANCE.toDto(e);
    }
    return nextRace;
  }
}

package com.gvc.oxygen.betreceipts.service;

import com.gvc.oxygen.betreceipts.config.NextRaceProps;
import com.gvc.oxygen.betreceipts.dto.MetaEvent;
import com.gvc.oxygen.betreceipts.entity.Bet;
import com.gvc.oxygen.betreceipts.entity.NextRace;
import com.gvc.oxygen.betreceipts.entity.NextRacesResult;
import com.gvc.oxygen.betreceipts.entity.TypeFlagCodes;
import com.gvc.oxygen.betreceipts.utils.NextRacesConstants;
import java.time.Duration;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeSet;
import java.util.concurrent.CompletableFuture;
import java.util.stream.Collectors;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;
import reactor.core.publisher.Mono;

@Slf4j
@Service
@RequiredArgsConstructor
public class NextRacesPublicService {

  private final EventService eventService;

  private final BetService betService;

  private final NextRaceProps nextRaceProps;

  /**
   * Method that look for next available racing post tip for next races. * It looks for first
   * configured time period races and give priority to the UK and IRE races. * If we don't have tips
   * available then, It looks for available races for today and tomorrow. * It also filters all the
   * races which user already placed bet. * If it couldn't find the tip. then it returns the next
   * races.
   *
   * @param username user whom we are showing tips.
   * @return Returns an object of {@link NextRacesResult}.
   */
  public NextRacesResult find(String username, boolean isTipEnabled) {
    return getNextRaceResult(username, isTipEnabled);
  }

  private NextRacesResult getNextRaceResult(String username, boolean isTipEnabled) {
    NextRacesResult result = new NextRacesResult();
    Mono<List<MetaEvent>> eventFlux =
        eventService.getMetaEvents().collectList().map(this::prioritizeByTimePeriod);
    log.debug("is tip enabled {}", isTipEnabled);

    if (isTipEnabled) {
      Mono<List<NextRace>> nextRaces = getTipsForTodayRaces(eventFlux, username);
      // on success store first bet on current user.
      nextRaces =
          nextRaces
              .defaultIfEmpty(Collections.emptyList())
              .doOnSuccess(races -> handleResponse(username, races));

      nextRaces.subscribe(result::setRaces);
    }
    if (CollectionUtils.isEmpty(result.getRaces())) {
      getNextRaces(eventFlux).subscribe(result::setRaces);
      result.setNextRace(true);
      return result;
    }
    return result;
  }

  private void handleResponse(String username, List<NextRace> races) {
    if (!CollectionUtils.isEmpty(races)) {
      storeFirstTipToUser(username, races.get(0));
    }
  }

  /*
   * Always storing the first bet as shown against the user.
   */
  private void storeFirstTipToUser(String userName, NextRace nextRace) {
    CompletableFuture.runAsync(
        () -> {
          Bet bet = new Bet();
          bet.setEventIds(new TreeSet<>(Arrays.asList(nextRace.getId())));
          bet.setUsername(userName);
          betService.saveBet(bet, userName);
        });
  }

  private Mono<List<NextRace>> getTipsForTodayRaces(
      Mono<List<MetaEvent>> eventsFlux, String username) {
    return eventsFlux
        .map(events -> removeEventsFromBetHistory(events, username))
        .flatMapIterable(e -> e)
        .filter(MetaEvent::isTipAvailable)
        .map(MetaEvent::getEventId)
        .take(nextRaceProps.getMaxNextRaces())
        .collectList()
        .map(eventService::getEventsByIds);
  }

  private Mono<List<NextRace>> getNextRaces(Mono<List<MetaEvent>> events) {

    return events
        .flatMapIterable(event -> event)
        .map(MetaEvent::getEventId)
        .take(nextRaceProps.getMaxNextRaces())
        .collectList()
        .map(eventService::getEventsByIds);
  }

  /** Method that returns next 15 min. events */
  private List<MetaEvent> getNextEvents(List<MetaEvent> allEvents) {

    List<MetaEvent> nextEvents = new ArrayList<>();

    if (!CollectionUtils.isEmpty(allEvents)) {
      // Group the next events if we have UK or IRE give priority to them.
      nextEvents.addAll(
          filterNextEvents(
              allEvents, TypeFlagCodes.of(NextRacesConstants.UK, NextRacesConstants.IE)));

      nextEvents.addAll(filterNextEvents(allEvents, TypeFlagCodes.of(NextRacesConstants.INT)));
      log.info("Got next 15 min. events with size {}", nextEvents.size());
    }

    return nextEvents;
  }

  private List<MetaEvent> prioritizeByTimePeriod(List<MetaEvent> todayEvents) {
    Map<Integer, List<MetaEvent>> priorityEvents = getPriorityByTypeAndTime(todayEvents);
    return orderByPriority(priorityEvents);
  }

  private List<MetaEvent> orderByPriority(Map<Integer, List<MetaEvent>> priorityList) {
    List<MetaEvent> orderedList = new ArrayList<>();
    orderedList.addAll(getNextEvents(priorityList.get(0)));
    orderedList.addAll(priorityList.get(1));
    return orderedList;
  }

  private Map<Integer, List<MetaEvent>> getPriorityByTypeAndTime(List<MetaEvent> todayEvents) {
    Instant start = Instant.now();
    Map<Integer, List<MetaEvent>> priorityList = new HashMap<>();
    int i = 0;
    while (i < todayEvents.size() && isWithinTimePeriod(todayEvents.get(i))) {
      i++;
    }
    priorityList.put(0, todayEvents.subList(0, i));
    priorityList.put(1, todayEvents.subList(i, todayEvents.size()));
    log.info(
        "time: getPriorityByTypeAndTime {}", Duration.between(start, Instant.now()).toMillis());

    return priorityList;
  }

  private List<MetaEvent> removeEventsFromBetHistory(List<MetaEvent> events, String username) {
    log.debug("removeEventsFromBetHistory size {}", events.size());
    Instant start = Instant.now();
    Set<String> userHistoryEvents = getUserHorseRacingBetHistory(username);
    log.debug("removeEventsFromBetHistory user history count {}", userHistoryEvents.size());
    List<MetaEvent> metaEvent =
        events.stream()
            .filter(event -> !userHistoryEvents.contains(event.getEventId()))
            .collect(Collectors.toList());
    Instant end = Instant.now();

    log.debug(
        "time: removeEventsFromBetHistory:: time taken {}",
        Duration.between(end, start).toMillis());
    return metaEvent;
  }

  private Set<String> getUserHorseRacingBetHistory(String username) {
    Instant start = Instant.now();
    Bet bet = betService.findByUsername(username);
    log.info(
        "time: getUserHorseRacingBetHistory time {} ",
        Duration.between(start, Instant.now()).toMillis());
    if (bet != null) {
      return bet.getEventIds();
    } else {
      return Collections.emptySet();
    }
  }

  private List<MetaEvent> filterNextEvents(List<MetaEvent> allEvents, TypeFlagCodes of) {
    return allEvents.stream()
        .filter(e -> TypeFlagCodes.of(e.getTypeFlagCodes()).contains(of))
        .collect(Collectors.toList());
  }

  public boolean isWithinTimePeriod(MetaEvent event) {
    Instant startTime = event.getStartTime();
    return Instant.now()
        .plus(nextRaceProps.getTimePeriodMinutes(), ChronoUnit.MINUTES)
        .isAfter(startTime);
  }
}

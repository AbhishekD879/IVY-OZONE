package com.gvc.oxygen.betreceipts.scheduler;

import com.coral.oxygen.middleware.ms.liveserv.LiveServService;
import com.egalacoral.spark.siteserver.model.Children;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Outcome;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.gvc.oxygen.betreceipts.config.NextRaceProps;
import com.gvc.oxygen.betreceipts.dto.HorseDTO;
import com.gvc.oxygen.betreceipts.dto.MetaEvent;
import com.gvc.oxygen.betreceipts.dto.RaceDTO;
import com.gvc.oxygen.betreceipts.entity.Bet;
import com.gvc.oxygen.betreceipts.entity.NextRace;
import com.gvc.oxygen.betreceipts.entity.NextRaceMap;
import com.gvc.oxygen.betreceipts.exceptions.JsonSerializeDeserializeException;
import com.gvc.oxygen.betreceipts.mapping.NextRaceMapper;
import com.gvc.oxygen.betreceipts.service.BetService;
import com.gvc.oxygen.betreceipts.service.EventService;
import com.gvc.oxygen.betreceipts.service.NextEventsService;
import com.gvc.oxygen.betreceipts.service.df.DFService;
import com.ladbrokescoral.lib.masterslave.executor.MasterSlaveExecutor;
import java.io.IOException;
import java.time.Instant;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.concurrent.CompletableFuture;
import java.util.stream.Collectors;
import javax.validation.constraints.NotNull;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.context.annotation.Profile;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;
import org.springframework.util.CollectionUtils;
import reactor.core.publisher.Flux;

@Slf4j
@Component
@RequiredArgsConstructor
@Profile("!UNIT")
public class RacingPostScheduler {

  public static final int BUFFER_MAX_SIZE = 20;

  private final MasterSlaveExecutor masterSlaveExecutor;

  private final NextEventsService nextEventsService;

  private final NextRaceProps nextRaceProps;

  private final DFService dfService;

  private final ObjectMapper objectMapper;

  private final EventService eventService;

  private final LiveServService liveServService;

  private final NextRaceMapper nextRaceMapper;

  private final BetService betService;

  @Scheduled(fixedDelay = 1_000 * 60 * 60 * 8)
  public void saveSiteservEvents() {
    masterSlaveExecutor.executeIfMaster(this::saveNextRaces, this::slaveAction);
  }

  @Scheduled(cron = "${app.bets.cron}")
  public void updateUserHistory() {
    masterSlaveExecutor.executeIfMaster(this::deleteUserExpiredHistory, this::slaveAction);
  }

  public void deleteUserExpiredHistory() {
    log.info("deleting user history");
    eventService
        .getMetaEvents()
        .map(MetaEvent::getEventId)
        .buffer()
        .subscribe(this::filerBetHistory);
  }

  public void filerBetHistory(List<String> events) {
    betService
        .findAllBets()
        .map(bet -> removeExpiredEvents(events, bet))
        .buffer(BUFFER_MAX_SIZE)
        .map(betService::updateBets)
        .subscribe();
  }

  public Bet removeExpiredEvents(List<String> eventIds, Bet bet) {
    Set<String> bets = bet.getEventIds();
    bets = bets.stream().filter(eventIds::contains).collect(Collectors.toSet());
    bet.setEventIds(bets);
    return bet;
  }

  private NextRace mapToNextRace(Event event, Map<Long, RaceDTO> races) {
    Optional<RaceDTO> raceDTO = Optional.ofNullable(races.get(Long.parseLong(event.getId())));
    if (raceDTO.isPresent()) {
      return nextRaceMapper.toDto(event, raceDTO.get());
    }
    return nextRaceMapper.toDto(event);
  }

  private List<Long> fetchIds(@NotNull List<Event> events) {
    return events.stream()
        .map(event -> Long.parseLong(event.getId()))
        .collect(Collectors.toCollection(ArrayList::new));
  }

  private void saveNextRaces() {
    Flux<Event> events = nextEventsService.getNextEvents();

    eventService.deleteAllMetaEvents();
    events
        .buffer(BUFFER_MAX_SIZE)
        .map(this::fetchDfData)
        .map(this::subScribeLiveUpdatesForTippedOutcomes)
        .map(this::eventsToNextRaceMaps)
        .map(eventService::saveNextRaceMap)
        .subscribe(eventMaps -> log.info("nextRaces saved to db..."));
    // event metadata can be refreshed on alternate executions...

  }

  private List<NextRace> fetchDfData(List<Event> events) {
    try {
      List<Long> ids = fetchIds(events);
      Map<Long, RaceDTO> races =
          dfService.getNextRaces(nextRaceProps.getCategoryId(), ids).orElse(new HashMap<>());

      return events.stream()
          .map(event -> mapToNextRace(event, races))
          .collect(Collectors.toCollection(ArrayList::new));
    } catch (IOException e) {
      log.error("error while fetching df data ", e);
    }

    return Collections.emptyList();
  }

  public void saveMetaEvent(List<MetaEvent> nextRaces) {
    // refresh events...
    eventService.saveMetaEvents(nextRaces);
  }

  private NextRaceMap eventToNextRaceMap(NextRace nextRace) {
    NextRaceMap nextRaceMap = null;
    try {
      nextRaceMap = new NextRaceMap(nextRace.getId(), objectMapper.writeValueAsString(nextRace), 1);
    } catch (JsonProcessingException exception) {
      throw new JsonSerializeDeserializeException(
          "Error in Serialization from nextRace obj", exception.getCause());
    }
    return nextRaceMap;
  }

  private List<NextRaceMap> eventsToNextRaceMaps(List<NextRace> nextRaces) {
    return nextRaces.stream()
        .map(this::eventToNextRaceMap)
        .collect(Collectors.toCollection(ArrayList::new));
  }

  private MetaEvent eventToMetaEvent(NextRace nextRace, boolean hasTip) {
    MetaEvent metaEvent = new MetaEvent();
    metaEvent.setEventId(nextRace.getId());
    metaEvent.setTypeFlagCodes(nextRace.getTypeFlagCodes());
    metaEvent.setStartTime(Instant.parse(nextRace.getStartTime()));
    metaEvent.setTipAvailable(hasTip);
    return metaEvent;
  }

  private List<NextRace> subScribeLiveUpdatesForTippedOutcomes(List<NextRace> nextRaces) {
    List<MetaEvent> metaEvents = new ArrayList<>();
    for (NextRace nextRace : nextRaces) {
      try {
        subScribeToEvents(metaEvents, nextRace);
      } catch (Exception ex) {
        log.error("error while fetching liveserv channels for subscription", ex);
      }
      CompletableFuture.runAsync(() -> saveMetaEvent(metaEvents));
    }
    return nextRaces;
  }

  private void subScribeToEvents(List<MetaEvent> metaEvents, NextRace nextRace) {
    liveServService.subscribe(
        nextRace.getLiveServChannels().substring(0, nextRace.getLiveServChannels().length() - 1));
    Optional<String> horseName = getTippedHorseSaddle(nextRace);
    if (horseName.isPresent()) {
      subscribeToOutcome(metaEvents, nextRace, horseName.get());
    } else {
      metaEvents.add(eventToMetaEvent(nextRace, false));
    }
  }

  private void subscribeToOutcome(List<MetaEvent> metaEvents, NextRace nextRace, String horseName) {
    metaEvents.add(eventToMetaEvent(nextRace, true));
    Optional<String> channel = getLiveServeChannelForRunnerNumber(horseName, nextRace);
    if (channel.isPresent()) {
      liveServService.subscribe(channel.get().substring(0, channel.get().length() - 1));
    }
  }

  private Optional<String> getTippedHorseSaddle(NextRace raceEvent) {
    if (!CollectionUtils.isEmpty(raceEvent.getHorses())) {

      return raceEvent.getHorses().stream()
          .filter(e -> Boolean.TRUE.equals(e.getIsMostTipped()))
          .map(HorseDTO::getHorseName)
          .findAny();
    }
    return Optional.empty();
  }

  private Optional<String> getLiveServeChannelForRunnerNumber(String horseName, NextRace nextRace) {
    List<Children> childrens = nextRace.getMarkets().get(0).getChildren();

    return childrens.stream()
        .map(Children::getOutcome)
        .filter(outcome -> outcome.getName().equalsIgnoreCase(horseName))
        .map(Outcome::getLiveServChannels)
        .findAny();
  }

  private void slaveAction() {
    log.debug("Slave action");
  }
}

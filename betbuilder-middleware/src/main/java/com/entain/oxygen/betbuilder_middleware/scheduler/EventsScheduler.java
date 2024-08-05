package com.entain.oxygen.betbuilder_middleware.scheduler;

import com.egalacoral.spark.siteserver.model.Event;
import com.entain.oxygen.betbuilder_middleware.exception.EmptySiteserveDataException;
import com.entain.oxygen.betbuilder_middleware.exception.ZookeeperException;
import com.entain.oxygen.betbuilder_middleware.repository.RedissonCombinationRepository;
import com.entain.oxygen.betbuilder_middleware.repository.RedissonEventIdRepository;
import com.entain.oxygen.betbuilder_middleware.service.SiteServeService;
import com.ladbrokescoral.lib.leader.LeaderStatus;
import java.time.Instant;
import java.util.*;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

@Service
public class EventsScheduler {
  private static final Logger ASYNC_LOGGER = LogManager.getLogger();
  private SiteServeService siteserveService;
  private RedissonCombinationRepository redissonCombinationRepository;
  private RedissonEventIdRepository redissonEventIdRepository;
  private LeaderStatus leaderStatus;

  @Autowired
  public EventsScheduler(
      RedissonCombinationRepository redissonCombinationRepository,
      RedissonEventIdRepository redissonEventIdRepository,
      SiteServeService siteserveService,
      LeaderStatus leaderStatus) {
    this.redissonCombinationRepository = redissonCombinationRepository;
    this.redissonEventIdRepository = redissonEventIdRepository;
    this.siteserveService = siteserveService;
    this.leaderStatus = leaderStatus;
  }

  @Scheduled(cron = "${event.cron.expression}")
  public void executeTask() {
    try {
      if (leaderStatus.isLeaderNode()) {
        ASYNC_LOGGER.info("Running scheduler at {}", Instant.now());
        getEventsFromSS()
            .doOnNext(this::purgeCombinationAndEventData)
            .switchIfEmpty(
                Mono.error(new EmptySiteserveDataException("Null data received from Siteserve")))
            .doOnError(
                error -> ASYNC_LOGGER.error("Error received from Siteserve {}", error.getMessage()))
            .subscribe();
      } else {
        slaveAction();
      }
    } catch (ZookeeperException e) {
      ASYNC_LOGGER.error(
          "Caught error while zookeeper leader election execution: {}", e.getMessage());
    }
  }

  public void slaveAction() {
    ASYNC_LOGGER.info("Slave");
  }

  private Mono<List<Event>> getEventsFromSS() {
    return siteserveService.getFinishedEvents();
  }

  private void purgeCombinationAndEventData(List<Event> ssEvents) {
    redissonEventIdRepository
        .readEvents()
        .map(
            (Map<String, String> eventsMap) ->
                ssEvents.stream().map(Event::getId).filter(eventsMap::containsKey).toList())
        .doOnNext(
            (List<String> eventIds) ->
                eventIds.forEach(
                    oEid ->
                        redissonCombinationRepository
                            .getCombinationsByOeId(oEid)
                            .doOnNext(
                                (List<Object> sgpIds) -> {
                                  ASYNC_LOGGER.info(
                                      "Purging {} combinations of event Id {}",
                                      sgpIds.size(),
                                      oEid);
                                  redissonCombinationRepository.deleteCombinations(oEid, sgpIds);
                                  redissonEventIdRepository.delete(oEid).subscribe();
                                })
                            .subscribe()))
        .subscribe();
  }
}

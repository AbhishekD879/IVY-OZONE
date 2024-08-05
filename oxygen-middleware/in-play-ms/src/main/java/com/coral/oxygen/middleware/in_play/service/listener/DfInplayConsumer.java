package com.coral.oxygen.middleware.in_play.service.listener;

import com.coral.oxygen.middleware.in_play.service.TopicContentConverter;
import com.coral.oxygen.middleware.in_play.service.model.safbaf.Entity;
import com.coral.oxygen.middleware.in_play.service.model.safbaf.Meta;
import com.coral.oxygen.middleware.in_play.service.scoreboards.ScoreBoardProcessor;
import com.coral.oxygen.middleware.in_play.service.siteserver.InplaySiteServeService;
import com.egalacoral.spark.siteserver.model.Category;
import com.egalacoral.spark.siteserver.model.Event;
import com.ladbrokescoral.lib.leader.LeaderStatus;
import java.util.List;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.cache.Cache;
import org.springframework.cache.CacheManager;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.messaging.handler.annotation.Header;
import org.springframework.stereotype.Service;

@Slf4j
@Service
public class DfInplayConsumer {
  private final TopicContentConverter converter;
  private final InplaySiteServeService siteServeService;
  private static final String VIRTUAL_SPORTS = "virtualSports";
  private static final String VIRTUAL_SPORT_CACHE = "virtualSportsCache";
  private final CacheManager cacheManager;
  private final LeaderStatus leaderStatus;

  private final List<String> supportedScoreBoardSports;

  private final ScoreBoardProcessor scoreBoardProcessor;

  public DfInplayConsumer(
      TopicContentConverter converter,
      InplaySiteServeService siteServeService,
      CacheManager cacheManager,
      ScoreBoardProcessor scoreBoardProcessor,
      LeaderStatus leaderStatus,
      @Value("${df.supported.scbrd.sports}") List<String> supportedScoreBoardSports) {
    this.converter = converter;
    this.siteServeService = siteServeService;
    this.cacheManager = cacheManager;
    this.scoreBoardProcessor = scoreBoardProcessor;
    this.leaderStatus = leaderStatus;
    this.supportedScoreBoardSports = supportedScoreBoardSports;
  }

  @KafkaListener(
      topics = "${df.scoreboard.topic.name}",
      containerFactory = "filteredKafkaScoreBoardsContainerFactory")
  public void consumeScoreboard(
      @Header(name = "${inplay.topic.eventKey}") Optional<String> obEventId,
      ConsumerRecord<String, String> scoreboardUpdate) {
    try {
      if (leaderStatus.isLeaderNode()) {
        processSafUpdates(scoreboardUpdate);
      } else {
        slaveAction();
      }
    } catch (Exception e) {
      log.warn("Caught error while zookeeper leader election execution", e);
    }
  }

  @KafkaListener(
      topics = "${df.scoreboards.topic}",
      containerFactory = "filteredKafkaScoreBoardsContainerFactory")
  public void consumeDfScoreBoard(
      @Header(name = "${scoreboard.topic.eventKey}") Optional<String> obEventId,
      @Header(name = "${scoreboard.topic.sport}") Optional<String> obSport,
      ConsumerRecord<String, String> scoreBoardRecord) {
    try {
      log.info(
          "DfInplayConsumer::Incoming Score board update from DF::{}", scoreBoardRecord.value());
      obSport.ifPresent(
          (String sport) -> {
            if (supportedScoreBoardSports.contains(sport.toLowerCase())) {
              obEventId.ifPresent(
                  (String eventId) ->
                      this.scoreBoardProcessor.processScoreBoardData(
                          eventId, scoreBoardRecord.value()));
            }
          });

    } catch (Exception e) {
      log.warn("Caught error while zookeeper leader election execution", e);
    }
  }

  public void processSafUpdates(ConsumerRecord<String, String> scoreboardUpdate) {
    log.info("Started saf");
    Optional<Entity> entity = converter.convertSafUpdateToPojo(scoreboardUpdate.value());
    if (entity.isPresent() && entity.get().getMeta() != null) {
      Meta meta = entity.get().getMeta();
      if (meta.getParents() != null && meta.getParents().split(":")[0].contains("39")) {
        log.info("Started saf with Category ID 39 :");
        List<Category> categoriesforVirtualHub = siteServeService.getClassesforVirtualHub();

        List<String> classIds =
            categoriesforVirtualHub.stream().map(cv -> cv.getId().toString()).toList();

        List<Event> virtualEvents = siteServeService.getVirtualEvents(classIds);
        Cache cache = cacheManager.getCache(VIRTUAL_SPORT_CACHE);
        log.info("Cache data in Consumer :" + cache);
        if (cache != null) {
          cache.put(VIRTUAL_SPORTS, virtualEvents);
        }
      }
    }
  }

  public void slaveAction() {
    log.info("Slave");
  }
}

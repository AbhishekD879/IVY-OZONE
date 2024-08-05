package com.coral.oxygen.middleware.in_play.service;

import com.coral.oxygen.middleware.common.service.ChangeDetector;
import com.coral.oxygen.middleware.common.service.notification.MessagePublisher;
import com.coral.oxygen.middleware.common.service.notification.topic.TopicType;
import com.coral.oxygen.middleware.in_play.service.config.InPlayDataProcessorConfig;
import com.coral.oxygen.middleware.in_play.service.market.selector.MarketSelectorService;
import com.coral.oxygen.middleware.in_play.service.model.CompetitionDifferenceBuilder;
import com.coral.oxygen.middleware.in_play.service.model.InPlayCache;
import com.coral.oxygen.middleware.in_play.service.model.SportCompetitionChanges;
import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayData;
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment;
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportsRibbon;
import com.google.gson.Gson;
import com.newrelic.api.agent.NewRelic;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class InPlayDataProcessor {
  private final InPlayDataConsumer consumer;
  private final InPlayStorageService storageService;
  private final InPlayDataSorter inPlayDataSorter;
  private final MessagePublisher messagePublisher;
  private final InplayLiveServerSubscriber inplayLiveServerSubscriber;
  private final MarketSelectorService marketSelectorService;
  private final boolean isPessimisticModeEnabled;

  private final Gson gson;

  public InPlayDataProcessor(InPlayDataProcessorConfig.InPlayDataProcessorBuilder builder) {
    this.consumer = builder.getConsumer();
    this.storageService = builder.getStorageService();
    this.messagePublisher = builder.getMessagePublisher();
    this.inplayLiveServerSubscriber = builder.getInplayLiveServerSubscriber();
    this.marketSelectorService = builder.getMarketSelectorService();
    this.gson = builder.getGson();
    this.isPessimisticModeEnabled = builder.isPessimisticModeEnabled();
    this.inPlayDataSorter = builder.getInPlayDataSorter();
  }

  public void tryProcess() {
    try {
      process();
    } catch (Exception e) {
      this.onError(e);
    }
  }

  private void process() {
    InPlayData data = consumer.consume();
    // subscribe to liveserver updates
    inplayLiveServerSubscriber.subscribe(data.getLivenow());
    inplayLiveServerSubscriber.subscribe(data.getUpcoming());
    saveAndNotifyOnChange(data);
  }

  private void saveAndNotifyOnChange(InPlayData data) {
    // reading previous stored InPlay cache
    InPlayCache previousCache = storageService.getLatestInPlayCache();
    // reading previous stored data before storing new one
    InPlayData previousStructure = storageService.getLatestInPlayDataObject();
    SportsRibbon previousRibbon = storageService.getLatestSportsRibbonObject();

    // extract sport segments to be stored separately
    List<SportSegment> sportSegments =
        InPlayData.allSportSegmentsStream(data)
            .map(marketSelectorService::splitByMarketSelectors)
            .flatMap(Collection::stream)
            .collect(Collectors.toCollection(ArrayList::new));

    inPlayDataSorter.sort(sportSegments);

    SportsRibbon sportsRibbon = data.getSportsRibbon();
    InPlayData structure = cloneStructureWithoutSegmentTypesAndRibbons(data);

    // save current data
    long generation = storageService.save(structure, sportSegments, sportsRibbon);
    storageService.clearError();
    structureChangesDetectAndPublish(generation, structure, previousStructure);
    competitionChangesDetectAndPublish(generation, previousCache);
    sportsRibbonChangesDetectAndPublish(generation, sportsRibbon, previousRibbon);
    virtualSportsRibbonChangeDetectAndPublish(generation, structure, previousStructure);
  }

  private void virtualSportsRibbonChangeDetectAndPublish(
      long generation, InPlayData structure, InPlayData previousStructure) {

    boolean changeDetected =
        ChangeDetector.isVirtualEventsChanged(
            previousStructure.getVirtualSportEvents(), structure.getVirtualSportEvents());
    log.debug("Change detector value is : " + changeDetected);
    if (isPessimisticModeEnabled || !changeDetected) {
      log.debug("[InPlayDataProcessor:VIRTUAL_SPORTS_RIBBON_CHANGED] #{}", generation);
      messagePublisher.publish(TopicType.VIRTUAL_SPORTS_RIBBON_CHANGED, String.valueOf(generation));
    }
  }

  private void sportsRibbonChangesDetectAndPublish(
      long generation, SportsRibbon sportsRibbon, SportsRibbon previousRibbon) {
    // check sports ribbon change
    if (ChangeDetector.changeDetected(sportsRibbon, previousRibbon)) {
      log.debug("IN_PLAY_SPORTS_RIBBON_CHANGED: {}", generation);
      messagePublisher.publish(TopicType.IN_PLAY_SPORTS_RIBBON_CHANGED, String.valueOf(generation));
    }
  }

  private void competitionChangesDetectAndPublish(long generation, InPlayCache previousCache) {
    // create diff between caches a new and the old one.
    if (previousCache != null) {
      InPlayCache thisCache = storageService.getLatestInPlayCache();
      Collection<SportCompetitionChanges> competitionChanges =
          CompetitionDifferenceBuilder.builder()
              .generation(generation)
              .compareCaches(thisCache, previousCache)
              .build();
      if (!competitionChanges.isEmpty()) {
        final String changes = gson.toJson(competitionChanges);
        log.info("IN_PLAY_SPORT_COMPETITION_CHANGED: {}", changes);
        messagePublisher.publish(TopicType.IN_PLAY_SPORT_COMPETITION_CHANGED, changes);
      }
    }
  }

  private void structureChangesDetectAndPublish(
      long generation, InPlayData structure, InPlayData previousStructure) {
    // check structure change
    if (isPessimisticModeEnabled
        || ChangeDetector.changeDetected(structure, previousStructure, true)) {
      log.debug("[InPlayDataProcessor:IN_PLAY_STRUCTURE_CHANGED] #{}", generation);
      messagePublisher.publish(TopicType.IN_PLAY_STRUCTURE_CHANGED, String.valueOf(generation));
    }
  }

  private InPlayData cloneStructureWithoutSegmentTypesAndRibbons(InPlayData data) {
    // clone data and cut types from sport segments
    InPlayData structure = deepClone(data);
    InPlayData.allSportSegmentsStream(structure)
        .forEach(sport -> sport.setEventsByTypeName(Collections.emptyList()));
    structure.setSportsRibbon(null);
    return structure;
  }

  private void onError(Exception e) {
    NewRelic.noticeError(e);
    log.error("Error during InPlay data processing", e);
    storageService.saveError(e);
  }

  private InPlayData deepClone(InPlayData toBeCloned) {
    return gson.fromJson(gson.toJson(toBeCloned), toBeCloned.getClass());
  }
}

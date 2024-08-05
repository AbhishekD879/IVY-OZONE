package com.coral.oxygen.middleware.in_play.service.injector;

import com.coral.oxygen.middleware.in_play.service.scoreboards.ScoreboardCache;
import com.coral.oxygen.middleware.in_play.service.scoreboards.ScoreboardEvent;
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayData;
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment;
import com.egalacoral.spark.liveserver.utils.JsonMapper;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
@Slf4j
public class ScoreBoardStatsInjector implements InPlayDataInjector {
  private final List<Integer> supportedCategories;
  private final ScoreboardCache scoreboardCache;
  private final JsonMapper jsonMapper;

  public ScoreBoardStatsInjector(
      @Value("${scoreboard.categories}") List<Integer> supportedCategories,
      ScoreboardCache scoreboardCache,
      JsonMapper jsonMapper) {
    this.supportedCategories = supportedCategories;
    this.scoreboardCache = scoreboardCache;
    this.jsonMapper = jsonMapper;
  }

  @Override
  public void injectData(InPlayData inPlayData) {
    doInjectScoreBoardStats(inPlayData.getLivenow().getSportEvents());
  }

  private void doInjectScoreBoardStats(List<SportSegment> sportSegments) {
    sportSegments.forEach(
        (SportSegment sportSegment) -> {
          if (this.supportedCategories.contains(sportSegment.getCategoryId())) {
            sportSegment
                .getEventsByTypeName()
                .forEach(typeSegment -> populateInplayScoreBoardStats(typeSegment.getEvents()));
          }
        });
  }

  private void populateInplayScoreBoardStats(List<EventsModuleData> eventsModuleData) {
    eventsModuleData.forEach(
        (EventsModuleData moduleData) -> {
          log.debug("ScoreBoardStatsInjector::eventId is ::{}", moduleData.getId());
          this.scoreboardCache
              .findById(String.valueOf(moduleData.getId()))
              .ifPresent((ScoreboardEvent update) -> moduleData.setStatsAvailable(true));
        });
  }
}

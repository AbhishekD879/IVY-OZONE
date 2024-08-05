package com.coral.oxygen.middleware.in_play.service.injector;

import com.coral.oxygen.middleware.in_play.service.CMSDataInjector;
import java.util.EnumMap;
import java.util.Map;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class InPlayDataInjectorFactory {
  private final Map<InPlayDataInjectorType, InPlayDataInjector> injectorMap;

  @Autowired
  public InPlayDataInjectorFactory(
      InPlayEventCountInjector eventCountInjector,
      InPlayEventIdsInjector eventIdsInjector,
      SportsConfigDataInjector sportsConfigDataInjector,
      InplayCommentaryInjector commentaryInjector,
      TypeSectionTitleDataInjector sectionTitleDataInjector,
      CMSDataInjector cmsDataInjector,
      ScoreBoardStatsInjector scoreBoardStatsInjector) {
    this.injectorMap = new EnumMap<>(InPlayDataInjectorType.class);
    this.injectorMap.put(InPlayDataInjectorType.EVENT_COUNT, eventCountInjector);
    this.injectorMap.put(InPlayDataInjectorType.EVENT_IDS, eventIdsInjector);
    this.injectorMap.put(InPlayDataInjectorType.SPORTS_CONFIG, sportsConfigDataInjector);
    this.injectorMap.put(InPlayDataInjectorType.COMMENTARY, commentaryInjector);
    this.injectorMap.put(InPlayDataInjectorType.TYPE_SECTION_TITLE, sectionTitleDataInjector);
    this.injectorMap.put(InPlayDataInjectorType.CMS_SPORT_DATA, cmsDataInjector);
    this.injectorMap.put(InPlayDataInjectorType.SCORE_BOARD_STATS, scoreBoardStatsInjector);
  }

  public <T> InPlayDataInjector<T> injectorOf(InPlayDataInjectorType injectorType) {
    return (InPlayDataInjector<T>) injectorMap.get(injectorType);
  }
}

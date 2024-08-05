package com.coral.oxygen.middleware.in_play.service.injector;

import com.coral.oxygen.middleware.common.service.SportsConfig;
import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayData;
import org.springframework.stereotype.Component;

@Component
public class SportsConfigDataInjector implements InPlayDataInjector {

  private final SportsConfig sportsConfig;

  public SportsConfigDataInjector(SportsConfig sportsConfig) {
    this.sportsConfig = sportsConfig;
  }

  @Override
  public void injectData(InPlayData inPlayData) {
    InPlayData.allSportSegmentsStream(inPlayData)
        .forEach(
            sportSegment -> {
              String categoryId = String.valueOf(sportSegment.getCategoryId());
              SportsConfig.SportConfigItem configItem = sportsConfig.getBySportId(categoryId);
              if (configItem != null && configItem.getPath() != null) {
                sportSegment.setCategoryPath(configItem.getPath());
              }
            });
  }
}

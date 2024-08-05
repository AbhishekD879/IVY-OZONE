package com.ladbrokescoral.oxygen.trendingbets.service;

import com.ladbrokescoral.oxygen.trendingbets.dto.PopularBets;
import com.ladbrokescoral.oxygen.trendingbets.siteserv.SiteServeService;

public abstract class PersonalizedBetsService extends PopularBetsService {

  protected PersonalizedBetsService(
      LiveUpdatesService liveUpdatesService,
      SiteServeService siteServeService,
      String[] filterMarketDrilldownTagNames,
      String[] filterEventDrilldownTagNames) {
    super(
        liveUpdatesService,
        siteServeService,
        filterMarketDrilldownTagNames,
        filterEventDrilldownTagNames);
  }

  @Override
  protected PopularBets getBetType() {
    return PopularBets.PERSONALIZED_BETS;
  }
}

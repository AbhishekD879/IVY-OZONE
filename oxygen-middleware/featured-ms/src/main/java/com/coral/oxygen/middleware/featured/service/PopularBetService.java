package com.coral.oxygen.middleware.featured.service;

import com.coral.oxygen.middleware.pojos.model.cms.featured.PopularAccaWidgetData;
import com.coral.oxygen.middleware.pojos.model.output.popular_bet.PopularAccaResponse;
import com.coral.oxygen.middleware.pojos.model.output.popular_bet.TrendingBetsDto;

public interface PopularBetService {

  TrendingBetsDto getTrendingBetByChannel(String channelId);

  PopularAccaResponse getPopularAccaForData(PopularAccaWidgetData data);
}

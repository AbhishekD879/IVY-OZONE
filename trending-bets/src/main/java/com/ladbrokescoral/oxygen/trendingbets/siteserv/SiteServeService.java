package com.ladbrokescoral.oxygen.trendingbets.siteserv;

import com.ladbrokescoral.oxygen.trendingbets.dto.TrendingItem;
import java.util.List;
import reactor.core.publisher.Mono;

public interface SiteServeService {

  Mono<List<TrendingItem>> getEventToOutcomeForOutcome(List<TrendingItem> outcomesIds);
}
